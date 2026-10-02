# Credential Gate Rule Design

Gate pre-commit hanya berguna kalau polanya benar. Dua bug di bawah sama-sama
membuat gate terlihat hijau sementara kredensial asli melintas ke repo publik.

## 1. Word-boundary anchor yang salah pada nama env

Pola generik lama:

```python
re.compile(r"(?i)\b(api[_-]?key|secret|token|password|passwd|access[_-]?key)\b\s*[=:]\s*[\"'][A-Za-z0-9_\-]{24,}[\"']")
```

`\b` menyatakan batas kata. `_` adalah word character, jadi di dalam
`CAMOFOX_API_KEY` posisi sebelum `API_KEY` **bukan** batas kata — keduanya
menyambung lewat `_`.

```python
re.compile(r"\b(api_key)") .search("CAMOFOX_API_KEY=...")   # tidak cocok
```

Akibatnya setiap nama env bergaya `SCREAMING_SNAKE` otomatis kebritish:
`GITHUB_TOKEN`, `NINE_ROUTER_API_KEY`, `CAMOFOX_ADMIN_KEY`, `PI_API_KEY`.
Persis kelas yang paling rawan, karena itu yang dipakai untuk CI dan layanan.

Perbaikan: ganti jangkar `\b` dengan run prefiks eksplisit.

```python
# \b  atau prefiks env uppercase
r"(?i)(?:\b|[A-Z0-9]+_)(?:api[_-]?key|admin[_-]?key|secret|token|password|passwd|access[_-]?key)"
```

Alt `[A-Z0-9]+_` tetap case-insensitive lewat `(?i)`, sehingga
`my_api_key` tetap tertangkap juga.

## 2. Ambang panjang di atas panjang key sebenarnya

`{24,}` adalah tebakan. Kalau key shortest milikmu 19 karakter, gate tidak akan
pernah menyentuhnya.

Cara menentukan ambang yang benar: ukur key terpendek yang benar-benar kamu pakai,
lalu turunkan sedikit di bawahnya.

```bash
# panjang tiap nilai env, tanpa mencetak nilai
awk -F= '/^[A-Z_]+=/{print length($2), $1}' ~/.hermes/.env | sort -n | head
```

Dengan ambang 16, key 19 dan 25 karakter keduanya tertangkap; placeholder
pendek seperti `your-key-here` tetap lolos.

## 3. Varian nama yang absen dari daftar

`access_key` ada di pola, `admin_key` tidak. Kalau key admin ikut bocor, gate
tidak akan melihatnya. Saat menambah pola, zip daftar nama dengan env yang
benar-benar ada di mesin:

```bash
grep -oE "^[A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD)" ~/.hermes/.env | tr -d '='
```

## 4. Gate yang meng-regenerasi kebocoran sendiri

Pola paling berbahaya adalah pipeline yang menulis secret ke repo setiap kali
dijalankan — gate akan menolak commit hari itu, lalu commit berikutnya tetap
melewat begitu jemand bypass sekali saja.

Di DR repo, `build-services.sh` menyalin plist launchd live dengan satu
perintah substitusi path:

```bash
sed -e "s|$HOME|{{HOME}}|g" "$src" > "$OUT/$a.plist.template"
```

Plist `ai.hermes.camofox.plist` memuat `CAMOFOX_API_KEY`, `CAMOFOX_ACCESS_KEY`,
dan `CAMOFOX_ADMIN_KEY` di `EnvironmentVariables`. Ketiganya ikut ter-copy apa
adanya. Setiap `sync-all.sh` menulis ulang secret ke riwayat git.

Perbaikannya bukan "tambah pola gate", tapi hentikan sumbernya: redaksi sebelum
freeze, lalu verifikasi hasilnya sebagai langkah terpisah.

```bash
# verifikasi wajib: kalau redaction gagal diam-diam, secret bocor tanpa alarm
if grep -qE '^[^<]*(KEY|TOKEN|SECRET|PASSWORD)=[^<]{16,}' "$OUT" ; then
  echo "REDACTION FAILED" >&2; exit 1
fi
```

Redaksi berbasis nama key lebih rapi ditulis dengan awk (mendeteksi `<key>` lalu
mengganti `<string>` berikutnya) daripada sed, karena BRE tidak punya operator
non-capturing sehingga pola key/nilai jadi kabur.

## 5. Kunci dengan self-test dari fragmen

Fixture yang meniru kebocoran asli juga akan memicu gate pada file test itu
sendiri. Susun dari potongan runtime supaya tidak ada baris `NAMA_KEY=nilai`
utuh di repo:

```python
V_API = "API" + "_KEY"
S1 = "cfapi" + "-" + "synthetic0"
MUST_CATCH = [("camofox_api", f'{P_CAMO}="{S1}"')]
```

Uji dua arah. Gate yang terlalu ketat menghasilkan commit sah yang ditolak,
dan orang cenderung membypass — hasil akhirnya lebih buruk dari gate yang longgar:

```python
raise SystemExit(1) if fails else 0
```

Lokasi: `scripts/secret-scan-staged.py` dan `scripts/test-secret-scan.py`
(repo `Niumination/ecosystem-config`).

## Daftar periksa sebelum percaya gate

- [ ] Namanya berisi prefiks env uppercase (`CAMOFOX_`, `GITHUB_`), bukan hanya kata tunggal
- [ ] Ambang panjang di bawah atau sama dengan key terpendek yang kamu pakai
- [ ] Semua varian nama yang ada di mesin ikut masuk daftar
- [ ] Tidak ada skrip di repo yang menyalin secret dari luar ke dalam
- [ ] Self-test ada, dua arah (harus tertangkap / harus lolos), exit non-zero saat gagal
- [ ] Gate benar-benar terpasang: `git config core.hooksPath .githooks`