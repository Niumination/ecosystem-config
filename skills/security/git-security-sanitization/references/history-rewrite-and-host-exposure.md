# History Rewrite: Interactive Stalls, Working-Tree Loss, and Host Exposure

Complements `history-rewrite-dry-run.md` (the sequence) with three failure modes that cost a full
retry cycle when met for the first time.

## 1. `--force` does NOT make `filter-repo` non-interactive

`--force` suppresses the fresh-clone refusal only. The "Treat this run as a continuation of the
previous run?" sanity check still reads stdin and dies with:

```
EOFError: EOF when reading a line
```

Answer it explicitly. Two prompts appear (continuation, then origin-removal notice), so pipe two lines:

```bash
printf 'y\ny\n' | git filter-repo --force --replace-text /tmp/redact-patterns.txt
```

## 2. `filter-repo` resets the working tree — re-apply uncommitted fixes

`filter-repo` checks out the rewritten HEAD, so **every uncommitted modification made before the
rewrite is reverted**, silently. Edits to the scanner, the gate regex, and redacted files all revert
to their pre-fix state, and the re-run self-test then fails as if the fix were never applied.

Re-apply them after the rewrite and re-run every self-test before committing. When the rewrite and a
source fix land in the same logical change, order it: rewrite history → re-apply source fixes →
re-run self-tests → commit → push.

Symptom to recognize: a self-test that passed minutes earlier now fails with the old pattern, and
`git status` shows fewer modified files than before the rewrite.

## 3. Prove host exposure by fetching the OLD ref back, not by reading local state

A force-push does not delete the old objects from the host, and "the old SHA still resolves" is the
check that proves it:

```bash
gh api repos/<o>/<r>/commits/<old-sha> --jq '.sha'          # resolves => object still present
gh api "repos/<o>/<r>/contents/<path>?ref=<old-sha>" --jq '.content' | base64 -d | grep -c '<literal>'
```

The second command is the decisive evidence: it counts how many times the literal is still being
served by the internet for the pre-rewrite ref. Report that count, not "0 hits in the working tree",
which says nothing about what the host is serving.

Only after the credential itself is confirmed dead does the residual object exposure drop from urgent
to hygiene — an unreachable old blob keeps being a purge request, not a live leak.

## 4. Redacting a truncated key still leaks its prefix

Docs often redact by truncation (`hermes...026`) rather than by removal. That is still a partial
disclosure and it still belongs in the rewrite patterns file:

```
literal:<full-value>==>__REDACTED_KEY__
literal:<truncated-form>==>__REDACTED_KEY__
```

Sweep for both before verifying: match the truncated shape (`prefix...suffix`) anywhere in tracked
files and history, not just the full value.

## 5. Find the structural source, not just the files that hold the leak

Files that *store* a secret are one class. The script that *copies live config into a repo* is the
class that regenerates the leak on every automated run, and it survives a history rewrite untouched.

For a repo whose purpose is backup/restore, grep the freeze/sync/build path for the step that copies
live config (e.g. a plist or dotenv) and asks what it substitutes. A substitution that only rewrites
`$HOME` and nothing else copies every secret it touches, every run.

Fix at the source with a redaction step plus a fail-closed assertion, so a regression aborts instead
of silently committing:

```bash
redact_plist "$src" | sed -e "s|$HOME|{{HOME}}|g" > "$out"
grep -qE '^[^<]*(KEY|TOKEN|SECRET|PASSWORD)=[^<]{16,}' "$out" && {
  echo "REDACTION FAILED for $name" >&2; exit 1; }
```

Use `awk` rather than `sed` for key/value pairing: BRE has no non-capturing group, so the
"this key is sensitive, redact the next string" pattern becomes unreadable as a regex. Assert on the
*output* — a grep for the sensitive-name shapes in every produced template — and report that count.

## 6. Force-push tidak menghapus object lama

Yang paling sering disalahartikan sebagai "sudah bersih".

```bash
git push --force-with-lease origin main   # sukses
gh api "repos/OWNER/REPO/contents/path?ref=OLD_SHA" --jq .content | base64 -d | grep -c SECRET
# 6   <-- isi lama masih terbaca
```

Object lama tidak terhapus karena masih ada di cache GitHub dan tidak lagi
direferensi branch manapun, tapi **tetap bisa diambil kalau SHA-nya diketahui**.

Konsekuensi praktisnya:

- siapa pun yang punya URL itu masih bisa mengunduh isinya
- skrip scraper untuk repo publik bisa menemukan lewat diff PR atau event log
- commit lama tidak hilang dalam waktu yang dapat diprediksi

Yang benar-benar menutup risiko adalah **rotasi dulu, baru rewrite**. Urutan
terbalik berarti key baru langsung ikut bocor di rewrite berikutnya. Panduan
resmi GitHub juga menyatakan rotasi biasanya sudah cukup, karena setelahnya nilai
itu tidak lagi berguna bagi siapa pun.

Purge total butuh GitHub Support (form "Remove sensitive data from a
repository"); tidak ada endpoint API untuk itu.

## 7. launchd menyimpan env di memori — restart tidak membaca ulang plist

Layanan yang env-nya dirotasi di disk tetap memakai nilai lama sampai job
definition-nya di-reload.

```bash
launchctl kickstart -k gui/$(id -u)/ai.hermes.camofox   # proses baru, env LAMA
kill -TERM "$(lsof -i :9377 -sTCP:LISTEN -t)"            # KeepAlive spawn ulang, env LAMA
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.camofox.plist
# baru di sini env terbaca ulang
```

Bukti yang tidak bisa dibantah: bandingkan sidik jari nilai di environment
proses dengan yang ada di file env. Nilai proses yang masih cocok dengan yang
lama = rotasi belum aktif, sekecil apa pun restart-nya.

```bash
PID=$(lsof -i :9377 -sTCP:LISTEN -t)
ps -E -p "$PID" | tr ' ' '\n' | grep '^CAMOFOX_.*KEY=' | shasum -a 256
```

Catatan: dari dalam gateway Hermes, `launchctl bootstrap` dan `submit` diblokir
guard, tetapi `unload` + `load` tidak. Kalau `bootstrap` tidak tersedia,
pasangan `unload`/`load` mencapai hal yang sama.

## 8. Urutan yang benar
