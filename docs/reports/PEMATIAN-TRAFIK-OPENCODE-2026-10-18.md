# Mematikan Trafik OpenCode + Membersihkan Provider Tak Diinginkan — 18 Okt 2026

## Bagian 1 — Trafik `oc/*` Dihentikan

Sumber abuse traffic: **21 model `oc/*`** di `config.yaml` dan **7 combo** di 9router yang semuanya
berisi `oc/*`.

**Yang dikerjakan:**
```
config.yaml          : 21 baris model oc/* dibuang
9router combos       : 7 combo dikosongkan (semua anggotanya oc/*), ditandai "off-"
config.yaml          : rujukan combo mati -> Agnes (combo hidup, 2 anggota)
job 69fe96da4c90     : model combo-delegasi -> Agnes
job 034116abd040     : DI-PAUSE (penyebab oc/* kembali)
```

**Temuan penting — job sync menulis ulang config.** `Sync 9router models to config` berjalan tiap
30 menit dan **mengembalikan** 21 model `oc/*` ke `config.yaml` setelah saya buang. Tanpa
mempause job ini, pembersihan akan terhapus sendiri dalam 30 menit. Job di-pause pada 22:29:31.

**Verifikasi:**
```
config.yaml bebas rujukan OpenCode      : oc/*=0, opencode-combo=0
combo 9router memuat oc/*               : 0
job dengan model oc/*                   : tidak ada
job sync di-pause                       : ya
```

**Catatan:** 17 entri `oc/*` masih ada di katalog 9router (`kv` table). Tidak dihapus — katalog
bukan jalur trafik, dan tidak ada combo yang memakainya lagi.

## Bagian 2 — Provider Dibersihkan (CLI + Desktop)

### Temuan yang mengubah diagnosis

`opencode auth list` menampilkan 4 provider (OpenCode Go, AgentRouter, Anthropic, OpenCode Console).
**Itu DEFINISI, bukan kredensial.** Buktinya:
```
opencode auth list --format json → connections: [{"type": "env", "name": "OPENCODE_API_KEY"}]
opencode auth logout opencode   → "Pass a credential ID or label when running without an interactive terminal"
db credential                   → 0 baris
```

Artinya keempat baris itu akan **tetap tampil** selama OpenCode CLI terinstal — ia hanya
mendeklarasikan "provider ini *bisa* membaca variabel env X". Yang menentukan apakah ada akses adalah
apakah variabel itu benar-benar ter-set.

### Sumber sebenarnya dari variabel itu

```
~/.zshrc → $DOTFILES_DIR/shared/environment.sh
        → vault/secrets.zsh          ← SUMBER NYATA
```

`vault/secrets.zsh` (mode 600) berisi:
```
OPENCODE_API_KEY, ANTHROPIC_API_KEY, AGENTROUTER_API_KEY   ← dihapus
GH_TOKEN, HUANCHENG_API_KEY, NINE_ROUTER_API_KEY, CC_VAULT ← dipertahankan
```

**Yang dibersihkan:**
```
vault/secrets.zsh : 4 baris dihapus (3 export + 1 komentar)
.env Hermes       : 4 baris OPENCODE* (dari tugas sebelumnya)
auth.json         : entri "opencode" (dari tugas sebelumnya)
db credential     : OAuth "Personal" (dari tugas sebelumnya)
opencode.json     : provider.9router.options.apiKey (dari tugas sebelumnya)
```

**Verifikasi:**
```
login shell: ANTHROPIC/AGENTROUTER/OPENCODE = kosong
GH_TOKEN, HUANCHENG_API_KEY, NINE_ROUTER_API_KEY = tetap ADA
opencode.json: provider 9router utuh, model 9router/nous/... longcat
```

### Yang Dipertahankan

- **9router** — `opencode.json` masih memuat provider `9router` (model `9router/nous/meituan/longcat-2.5-preview:free`),
  `NINE_ROUTER_API_KEY` tetap ada, 9router merespons HTTP 200.
- **`zenmux`** di `auth.json` — layanan berbeda, bukan OpenCode.
- **`opencode serve`** — pid 5077 tetap berjalan; pekerjaan yang jalan di sana tidak diganggu.

## Sisa yang Perlu Tindakan Pemilik

1. **Desktop masih menampilkan 4 provider** — itu definisi, bukan kredensial. Setelah variabel env
   kosong, provider itu tidak punya akses. Hilang dari tampilan hanya jika OpenCode di-uninstall
   atau definisi provider dihapus dari instalasi.
2. **Proses `opencode serve` (pid 5077) masih memegang** ketiga variabel di RAM. Perlu restart manual
   (bukan unit launchd) agar benar-benar lepas.
3. **Blokir IP belum dicabut** — `oc/*` akan tetap 403 sampai OpenCode mencabut blokir terhadap
   IP `125.165.42.32`. Yang menghentikan trafik adalah pemadaman jalur di Bagian 1.

## Backup

```
~/.hermes/cache/scratch/oc-cleanup-20261018-215014/   (kredensial OpenCode)
~/.hermes/cache/scratch/oc-disable-20261018-222253/   (config.yaml + combos)
~/.hermes/cache/scratch/oc-cleanup2-20261018-223449/  (secrets.zsh)
```

## Verifikasi Akhir

```
BAGIAN 1  trafik oc/* terhenti        : 4/4 OK
BAGIAN 2  kredensial dibersihkan      : 5/5 OK
BAGIAN 3  9router utuh (dipertahankan): 3/3 OK
BAGIAN 4  opencode CLI hidup         : 1/1 OK
HASIL                                 : SEMUA TERCAPAI
```
