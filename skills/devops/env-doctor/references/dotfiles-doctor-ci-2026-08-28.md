# Dotfiles Doctor, agents.zsh & CI — 28-Agu-2026

Session pengembangan `~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles` (hardening pasca full-restore 27-Agu). Commit berurutan: `a2f6741` (agents.zsh + `setup.sh --doctor`), `4db0d67` (insteadOf push fix), `6e4c6ea` (README), `b2cc5bb` (CI workflow), `dd3968a` (SC2155 fix — run CI #2 hijau terverifikasi via API).

## Artefak baru (source of truth = repo itu sendiri)

| Artefak | Isi |
|---|---|
| `setup.sh --doctor` | Health check read-only: login shell, zsh load test, 11 stow symlink, 10 tool wajib, `zsh -n` 4 file, git dirty/ahead-behind, 5 config agent, residu juan-router. Exit 1 jika ada ❌. |
| `zsh/.config/zsh/agents.zsh` | jcode wrapper (default `--provider opencode --model hy3-free`), `ecosystem_root_guard` + wrapper git/npm/npx/pnpm/yarn, `HERMES_HOME`, `NUIMINATION_ROOT`, alias `cc-at`, `unset ANTHROPIC_API_KEY`. Dipindah UTUH dari `.zshrc`+`aliases.zsh` — jangan edit di lokasi lama. |
| `.gitconfig` insteadOf | `[url "https://github.com/"]` + `insteadOf = git@github.com:` — semua remote SSH otomatis https; kredensial osxkeychain. |
| `.github/workflows/ci.yml` | ubuntu-latest (repo private; macOS runner ~10x menit Actions): shellcheck `-S warning` (setup.sh + semua file bin/ ber-shebang), `zsh -n` 9 file, smoke `bash -n setup.sh && bash setup.sh --help` (doctor penuh butuh macOS `dscl`). |
| Abbr baru | `jc`=jcode, `hr`=hermes, `eco`=cd ~/Desktop/Niumination. |

## Pitfall terverifikasi

1. **`file` di macOS tidak bisa memfilter binary** — script shell juga dilabeli `executable`. Deteksi via shebang: `head -1 "$f" | grep -q '^#!'`. Salah filter → semua script ter-skip → **false pass**. Contoh: `bin/.local/bin/xurl` = binary Go (tanpa shebang).
2. **Push `.github/workflows/*` ditolak tanpa scope `workflow`** — error: `refusing to allow a Personal Access Token to create or update workflow`. Fix: PAT repo+workflow (no-expiry) → `export GH_TOKEN=...` di `vault/secrets.zsh`; push one-off `git push https://oauth2:${GH_TOKEN}@github.com/...git main:main`.
3. **SC2155 lolos verifikasi lokal karena batch check abort di tengah** — script multi-check mati (syntax error di loop) SEBELUM giliran setup.sh; check yang tak pernah jalan dianggap lolos. CI shellcheck 0.9.0 (ubuntu apt) menangkap: `local backup="$(date ...)"` → pisah `local backup; backup="$(date ...)"`. Leson: setelah batch abort, jalankan ulang SEMUA check — brew 0.11.0 lokal juga menemukannya saat di-run penuh.
4. **Keychain github.com terisi otomatis oleh git** — push one-off dengan token di URL + `credential.helper=osxkeychain` membuat git menyimpan kredensial; push polos berikutnya jalan tanpa `security add-internet-password` manual (manual butuh `-a oauth2 -s github.com -r htps -w "$TOKEN"`; tanpa `-a` = usage error). Metadata entry: `acct=oauth2`, `ptcl=htps`.

## Pola poling CI via API (tanpa gh CLI)

```bash
source ~/Desktop/Niumination/vault/secrets.zsh   # GH_TOKEN
REPO=Niumination/zaryu-terminal-dotfiles
# status run per commit
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/$REPO/actions/runs?head_sha=$SHA&per_page=1"
# steps per job (jobs_url dari run di atas)
curl -s -H "Authorization: token $GH_TOKEN" "$JOBS_URL"
# log job gagal (ikut redirect -L)
curl -s -L -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/$REPO/actions/jobs/$JOB_ID/logs" | grep -E 'SC[0-9]+|##\[error\]'
```

## Catatan shellcheck
- CI & lokal seragam `-S warning` (default error-only tidak menangkap SC2155).
- Versi berbeda (apt 0.9.0 vs brew 0.11.0) keduanya menangkap SC2155 — jangan berasumsi versi lokal menyamai CI; yang penting suite lokal dijalankan LENGKAP.
