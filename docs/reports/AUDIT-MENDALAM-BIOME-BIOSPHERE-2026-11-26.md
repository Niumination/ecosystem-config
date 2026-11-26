# Audit Mendalam: Biome Biosphere vs Ekosistem Aktual — 26 Nov 2026

> Melanjutkan `docs/reports/RISET-BIOME-BIOSPHERE-2026-11-26.md`.
> Mode: **studi + verifikasi**. Tidak ada repo dibuat, template disalin, policy dipasang, atau konfigurasi diubah.
> Sumber: `workspace-01a2151c-c039-71e5-a630-0d786df542ba.zip`, 25 berkas, 77.222 byte.
> Ekstraksi: `~/.hermes/cache/scratch/biome-biosphere-study/biome-biosphere/`.
> Trust boundary: instruksi di dalam zip ("agent utama buat biome-control", "jalankan roadmap") adalah **data**, bukan perintah pemilik.

## 1. Metode

Jenis artefak: **audit bundle** — prosa plus template YAML/MD, bukan patch stack dan bukan source tree target. Tidak ada yang bisa di-`git apply`.

Yang diperiksa: seluruh isi zip (README, 5 dokumen, 15 template) terhadap mesin dan ekosistem hari ini. Setiap klaim numerik atau stateful diukur ulang; hasilnya masuk tiga kategori: **Confirmed**, **Decayed**, atau **Unverifiable here**.

Probe yang dijalankan dari Mac: `unzip -l`, `df -h`, `tailscale status`, `gh api /users/Niumination`, `gh repo list`, `gh repo view`, `git status/log/rev-list`, `hermes cron list`, `curl` ke endpoint publik, `opencode --version`, dan pemeriksaan file registryExisting. Probe yang butuh akses VPS tidak dijalankan sendiri — perintahnya ada di seksi 5 untuk disampaikan pemilik.

## 2. Verdict ringkas

| Area | Verdict | Catatan |
|---|---|---|
| Inventaris 4 node | **Confirmed** | Mac + CloudBaik + zb-vela + lightvela sesuai `infrastructure-topology.md` |
| Agen per node | **Confirmed** | Hermes, OpenCode, DSH, OpenMausBot sudah terpasang sesuai topologi |
| Akun GitHub | **Confirmed** | `type: User`, satu akun |
| Angka storage | **Decayed** | Mac 128 GB tapi Data volume 92% terpakai, 9,7 Gi bebas — di bawah ambang kritis dokumen |
| Connectivity antar node | **Decayed** | Tailscale saat ini **stopped**; A2A tidak terjangkau (`000`, bukan lagi `401`) |
| 3 repo kontrol baru | **Decayed / blocked** | Belum ada dan dilarang freeze D-1013-05; juga duplikat kontrol yang sudah ada |
| Control plane existing | **Confirmed** | `ecosystem-config` sudah berisi 362 doc, 156 script, dan 269 skill |
| Backup/DR existing | **Confirmed** | `niumination-restore` PRIVATE + script eco-guard + registry DR |
| Secret gate | **Confirmed** | `.gitignore`, pre-commit secret scan, CI gate sudah ada |
| Kesiapan roadmap | **Decayed** | Semua manifest masih `draft`, banyak `VALIDATE` |

Dokumen ini **tidak layak dijalankan apa adanya**. Layak diambil sebagai konsep saja.

## 3. Audit per dokumen

### 3.1 README

Klaim "4 ekosistem terfragmentasi" — **Confirmed sebagian**. Node memang terpisah secara fisik, tetapi sudah ada `docs/registry/infrastructure-topology.md`, `BACKLOG.md`, `DECISIONS.md`, dan thread orkestrator 13902. Jadi "tidak ada registry pusat" **Decayed**.

Klaim "storage 128/50/50/20 GB" — **Decayed untuk Mac**, **Unverifiable here untuk tiga VPS**. Pengukuran Mac: `/dev/disk1s1` 128 Gi, 102 Gi used, 9,7 Gi avail, 92%; `/Volumes/Niumination` 171 Gi, 59 Gi avail. Angka 128 GB menyembunyikan dua volume dan tidak mencatat kondisi kritis.

Klaim "satu akun GitHub" — **Confirmed**: `gh api /users/Niumination` → `type: User`. Jumlah repo aktual 179, bukan angka lama 169 di topologi.

Klaim "tidak ada secret di Git" — **Confirmed secara kontrol**, bukan secara absolut: gate pre-commit dan CI sudah ada, tetapi dalam ekosistem pernah terjadi insiden kebocoran yang sudah ditangani.

### 3.2 01-MASTER-BLUEPRINT.md

Visi "satu akun GitHub, banyak habitat" cocok (`01:8-15`). Dampak fragmentasi (`01:26-32`) sebagian sudah tertangani oleh registry dan thread 13902.

Tujuan G1-G8 (`01:34-45`):
- G1 Unified Control — **blokir**: mensyaratkan `biome-control` baru.
- G2 Storage-Aware — **belum ada implementasi**. Policy dokumen akan langsung menandai Mac `critical` karena 9,7 Gi bebas.
- G3 GitHub-Centric Memory — **sudah ada** lewat docs/registry + git history.
- G4 Portable Task — **sebagian** lewat thread 13902 dan `delegate_task`.
- G5 Secure by Default — **sudah ada** gate secret.
- G6 Recoverable — **sudah ada** `niumination-restore` dan DR registry.
- G7 Observable — **sudah ada** up-eco, MIRAI, laporan harian.
- G8 Agent-Operable — **sebagian** lewat DM + thread, bukan control plane baru.

Model L0-L7 (`01:60-99`) adalah kereta konseptual yang rapi, tetapi bisa dipetakan ke artefak existing: L0 = SOUL/AGENTS, L1 = docs/registry, L2 = BACKLOG + cron + thread, L3 = skill bank, L4 = infrastructure-topology, L5 = hermes send/dispatch, L6 = pre-commit + DR, L7 = MIRAI/up-eco. Tidak perlu lapisan fisik baru.

Peta habitat (`01:91-99`) cocok untuk peran node, tapi angka storage usang. Peta organisme (`01:100-108`) cocok; `dsh` terpasang di CloudBaik dan zb-vela, `openmausbot` di keduanya, `opencode` v2.4.1 di Mac dan CloudBaik.

Risiko `01:139-149` valid. Yang paling mendesak bukan "storage VPS penuh", melainkan **Mac Data volume sudah 92%**.

Definisi suksus `01:151-158` mengharuskan pembuatan `biome-control` — **tidak bisa dipenuhi** tanpa override freeze eksplisit dan tanpa menduplikat kontrol existing.

### 3.3 02-ARCHITECTURE.md

Diagram high-level (`02:18-86`) bertumpu pada tiga repo baru. Karena ketiganya tidak ada dan freeze berlaku, seluruh diagram itu **hypothetical**.

Topologi `02:137-189` cocok dengan kenyataan, tapi mengasumsikan konektivitas `BC <--> MAC_H`, `BC <--> CB_O`, dll. Fakta hari ini: Tailscale **stopped**, A2A Mac→Lightvela tidak terjangkau (`curl` → `000`); sebelumnya ketika Tailscale up, responsnya `401 -32050 unauthorized`. Jadi jalur kontrol antar node **tidak aktif**.

Matriks kapabilitas (`02:190-204`) masuk akal: heavy ke Mac, coding ke CloudBaik, automation ke zb-vela, bot/light ke lightvela. Ini konsep terbaik dokumen dan bisa dipertahankan.

Taksonomi repo (`02:204-236`) mengusulkan `biome-control`, `biome-notes`, `biome-config-backup`. **Decayed/blocked**: ketiganya tidak ada, dan fungsinya sudah ada di `ecosystem-config`, `docs/`, dan `niumination-restore`.

Kontrak task (`02:249-268`) bagus: `task_id`, `type`, `priority`, `repo`, `target_node`, `status`, `output`, `constraints`. Bisa dipakai tanpa repo baru.

Alur `02:269-287` mengasumsikan node bisa `pull manifest/policy` dan `update status`. Tidak ada mekanisme itu hari ini; yang ada adalah `hermes send` (outbound-only), `delegate_task`, dan cron yang dipaused. Jadi alur ini **belum bisa berjalan**.

Storage design `02:291-302` memakai angka lama. Aturan "lightvela shallow + single task" **layak diadopsi**; angka reserve tidak.

ADR `02:327-335` masuk akal secara konsep. ADR-001 "GitHub sebagai control plane" benar, tapi control plane yang dimaksud harus `ecosystem-config`, bukan repo baru.

### 3.4 03-PRD.md

Deskripsi masalah (`03:12-26**) benar secara umum, tapi "belum ada taksonomi dan governance terpadu" **Decayed** — sudah ada `docs/registry/project-catalog.md`, `deployment-status.md`, `infrastructure-topology.md`, dan `DECISIONS.md`.

Non-goals (`03:38-45`) bijak: tidak ganti runtime, tidak migrasi semua repo, tidak simpan binary besar, tidak otomatisasi keputusan sensitif. Selaras dengan aturan kita.

Use cases UC-01 sampai UC-07 (`03:55-98`) masuk akal sebagai desain. UC-06 (backup sanitasi) dan UC-07 (recovery) **sudah tercakup** oleh eco-guard + `niumination-restore`.

FR-1 sampai FR-7 (`03:99-158`) adalah daftar kebutuhan yang bagus, tetapi FR-4 secara eksplisit memaksa tiga repo baru. **Tolak FR-4 apa adanya**; ganti dengan "registry hidup di `ecosystem-config`".

NFR (`03:160-170`) tidak bisa diverifikasi penuh sekarang; RPO 24 jam dan RTO 24 jam **Unverifiable here** tanpa jadwal backup aktual dan drill terakhir.

Open questions `03:218-233`:
1. "Repo mana untuk notes/config/backup?" — **sudah terjawab**: `docs/`, `niumination-restore`.
2. "Buat baru atau pakai existing?" — **jawaban yang benar: existing**.
3. "Token per repo?" — **sudah diatur** lewat env/keychain dan aturan secret.
4. "Mac always-on?" — **tidak**; aturan ekosistem: laptop bukan server.
5. "Notifikasi via Issue/Telegram?" — **keduanya sudah ada**.
6. "Batasan GitHub Actions/Storage/Release?" — **Unverifiable here**; butuh info dari owner.

Acceptance criteria `03:172-196`: "repo control plane dibuat" dan "minimal 1 tugas lewat alur baru" **tidak bisa dipenuhi** hari ini.

### 3.5 04-GOVERNANCE-AND-OPERATIONS.md

RACI (`04:14-37`) bagus, tapi peran "Agent Utama" belum terdefinisi formal di ekosistem kita; yang ada thread 13902 + DM owner. Perlu keputusan pemilik bila mau dipakai.

Aturan inti (`04:38-47`) sudah selaras: no secret in Git, storage budget, lightvela light-only, ephemeral workspace, audit, graceful block. Ini bisa diadopsi sebagai **prinsip**, bukan policy baru.

Storage budget (`04:48-78`) **Decayed**. Ambang Mac `<20 GB degraded`, `<15 GB critical`; hari ini 9,7 Gi bebas, jadi mac sudah critical menurut dokumen itu sendiri.

Security governance (`04:80-124`) selaras. Denylist (`04:97-115`) adalah subset dari `.gitignore` kita; jangan mengganti yang existing dengan yang lebih lemah.

Backup (`04:125-154`) **duplikat**. Weekly config snapshot, RPO 24h, RTO 24h, recovery drill kuartalan — ekosistem sudah punya eco-guard backup harian, `niumination-restore`, dan drill registry. Bedanya: rincian verifikasi restore perlu diperbarui, bukan dibangun ulang.

Task lifecycle (`04:155-169`) bagus dan bisa dipetakan ke `BACKLOG.md` + status task. Field `blocker` dan `cleanup` benar-benar berguna.

SOP `04:190-230` terlalu generik untuk dipakai langsung; perlu menyertakan Tailscale, CF Tunnel, dan A2A nyata.

### 3.6 05-ROADMAP-AND-IMPLEMENTATION.md

Fase 0 selesai sebagai draft — **Confirmed**. Fase 1 mensyaratkan pembuatan tiga repo — **blocked**. Fase 2 storage hygiene bisa dimulai tanpa repo baru, tetapi angkanya harus diukur ulang. Fase 3 backup/recovery **sebagian sudah berjalan**. Fase 4 automasi **tidak bisa dimulai** sebelum A2A/Tailscale dan cron diperbaiki.

Backlog P0-P3 (`05:161-190`) sebagian besar sudah tercakup oleh up-eco dan registry. Yang benar-benar baru: storage report baseline lintas node dan pengukuran ulang kapasitas.

Handoff checklist (`05:196-230`) meminta "konfirmasi 4 node aktif dan aksesnya". Ini **belum bisa dipenuhi** dari Mac karena Tailscale stopped dan akses VPS perlu verifikasi langsung.

## 4. Audit template `biome-control`

| Berkas | Verdict | Catatan |
|---|---|---|
| `.gitignore` | Partial | Denylist bagus, tapi lebih lemah dari `.gitignore` root kita yang juga menutup `vault/`, `**/vault/`, `credentials-backup.zip`, dan file PII tertentu. Jangan ganti; gabungkan hanya jika diperlukan. |
| `README.md` | Draft benar | Struktur jelas, status draft jujur. Tidak ada kode. |
| `nodes/mac-hermes.yml` | Decayed | `storage_gb: 128` tanpa sebutan dua volume. `always_on: false` benar sesuai aturan laptop bukan server. `account: <single-github-account>` belum diisi. |
| `nodes/vps-cloudbaik.yml` | Unverifiable here | Agent `opencode` + `dsh` sesuai topologi; kapasitas 50 GB dan status `always_on` butuh verifikasi VPS. |
| `nodes/vps-zbvela.yml` | Unverifiable here | Agent `hermes` + `dsh` + `openmausbot` sesuai topologi; kapasitas dan unit service butuh verifikasi. |
| `nodes/vps-lightvela.yml` | Confirmed sebagian | Peran light-only benar. Public IP mati; hanya CF tunnel yang hidup. Kapasitas 20 GB butuh verifikasi. |
| `agents/dsh.yml` | Confirmed | Peran controlled-shell selaras dengan DSH di CloudBaik/zbvela. |
| `agents/hermes-agent.yml` | Confirmed | Generalist orchestrator sesuai pemakaian di Mac/zbvela/lightvela. |
| `agents/opencode.yml` | Confirmed | Versi terpasang `opencode v2.4.1`; preferensi CloudBaik masuk akal. |
| `agents/openmausbot.yml` | Confirmed | Relay ringan sesuai peran di zbvela/lightvela. |
| `policies/routing.yml` | Confirmed konsep | R1-R5 logis; R5 lightvela guard layak dipertahankan. Tidak ada engine yang menjalankannya hari ini. |
| `policies/storage.yml` | Decayed | Budget berdasarkan angka lama. Mac sudah di bawah `critical_free_gb: 15`. |
| `policies/security.yml` | Partial | Per-node credential bagus; denylist lebih lemah dari milik kita. `allow_secrets_in_git: false` selaras. |
| `policies/backup.yml` | Duplicate | RPO/RTO 24h dan sanitasi sudah ada di ekosistem; beda hanya nama repo tujuan. |
| `runbooks/*.md` | Partial | Generic. Perlu menyertakan CF Tunnel, Tailscale, A2A, dan alamat node nyata. |
| `templates/task-intake.md` | Confirmed konsep | Field `blocker`, `cleanup`, `acceptance criteria` sepadan dengan kebutuhan kita. |

## 5. Kebutuhan data dari VPS / ekosistem lain

Bagian ini untuk disampaikan ke node terkait. **Semua perintah bersifat read-only dan tanpa secret.** Jangan tempelkan nilai token; laporkan hanya kesimpulan atau kode error.

### 5.1 CloudBaik — lewat SSH `vps-baik`

```bash
ssh vps-baik 'bash -lc "
hostname; uptime; uname -a;
df -h;
for c in hermes opencode dsh docker; do printf \"%s: \" \"$c\"; command -v \"$c\" || echo MISSING; done;
opencode --version 2>/dev/null || true;
systemctl --no-pager --type=service --state=running | grep -Ei \"cloudflared|dsh|cron|ssh|opencode\" || true;
crontab -l 2>/dev/null | head -30;
ls -ld /root/dsh-web 2>/dev/null || true;
"'
```

Yang dicari: kapasitas sebenarnya, versi `dsh`/`opencode`, apakah Hermes benar-benar absen, service apa yang jalan, dan apakah ada cleanup cron.

### 5.2 zb-vela — jalankan langsung di VPS

```bash
hostname; uptime; uname -a; df -h;
for c in hermes dsh openmausbot docker; do printf "%s: " "$c"; command -v "$c" || echo MISSING; done;
systemctl list-units --type=service --all --no-pager | grep -Ei 'a2a|hermes|maus|dsh|tailscale|cron' || true;
tailscale status 2>/dev/null || true;
ss -tlnp | head -30;
```

Untuk akar `401 -32050` pada A2A, cari unit service A2A dulu dari perintah di atas, lalu:

```bash
sudo journalctl -u '<unit-a2a>' --since '48 hours ago' --no-pager \
  | grep -iE 'unauthor|token|32050|reject' | tail -40
```

Laporkan **hanya alasan errornya**, bukan isi token. Ini blocker sebelum routing lintas node bisa dipercaya.

### 5.3 Lightvela — jalankan langsung di VPS

```bash
hostname; uptime; uname -a; df -h;
for c in hermes openmausbot docker; do printf "%s: " "$c"; command -v "$c" || echo MISSING; done;
systemctl list-units --type=service --all --no-pager | grep -Ei 'hermes|maus|tailscale|cron' || true;
tailscale status 2>/dev/null || true;
curl -sS -m 10 https://maus.abstract.biz.id/health; echo;
ss -tlnp | head -30;
```

Yang dicari: kapasitas 20 GB masih benar atau tidak, apakah Hermes dan OMB benar-benar aktif, dan apakah port publik masih tertutup.

### 5.4 Mac — sudah saya ukur, untuk referensi

```bash
df -h / /System/Volumes/Data /Volumes/Niumination
tailscale status
hermes cron list 2>&1 | grep -ci paused
A2A_TOKEN="$(sed -n '1p' vault/a2a-token.txt)"
curl -s -o /dev/null -w '%{http_code}\n' -m 12 \
  -H "Authorization: Bearer $A2A_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"message/send","params":{}}' \
  http://100.65.20.34:9900/
unset A2A_TOKEN
```

### 5.5 GitHub / keputusan pemilik

Perlu keputusan, bukan perintah: apakah freeze D-1013-05 mau di-override untuk membuat tiga repo? Rekomendasi saya: **tidak**. Fungsinya sudah ada.

## 6. Rekomendasi akhir

1. **Jangan jalankan roadmap dan jangan buat tiga repo.** Ini duplikasi + pelanggaran freeze.
2. **Petakan ke struktur existing**: node/agent manifest → `docs/registry/`; policy → registry yang sama; task lifecycle → `BACKLOG.md` + thread 13902; backup → `niumination-restore` + eco-guard.
3. **Perbaiki data storage dulu.** Mac Data volume 92% / 9,7 Gi bebas — sudah kritis menurut policy dokumen itu sendiri. Jangan pakai angka 128 GB sebagai dasar routing.
4. **Pulihkan konektivitas sebelum bicara routing otomatis.** Tailscale stopped; A2A tidak terjangkau. Minta log server-side dari zb-vela untuk `401 -32050`.
5. Ambil dua konsep tanpa struktur baru: aturan **lightvela = light only** dan field wajib **blocker + cleanup** pada task penting.
6. Satu perubahan per sesi. Jangan gabungkan storage policy, task lifecycle, dan manifest dalam satu commit.

## 7. Bukti pengukuran sesi ini

- `unzip -l <zip>` → 25 berkas, 77.222 byte
- `df -h /System/Volumes/Data` → 128 Gi, 102 Gi used, 9,7 Gi avail, 92%
- `df -h /Volumes/Niumination` → 171 Gi, 112 Gi used, 59 Gi avail, 66%
- `tailscale status` → `Tailscale is stopped.`
- `curl -m 12` ke `http://100.65.20.34:9900/` dengan token dari file privat → `000` (tidak terjangkau, bukan `401`)
- `gh api /users/Niumination --jq '{type,login}'` → `type: User`
- `gh repo list Niumination --limit 300 | wc -l` → 179
- `gh repo view Niumination/niumination-restore --json visibility` → PRIVATE
- `hermes cron list | grep -ci paused` → 25
- `opencode --version` → `opencode v2.4.1`
- Endpoint: `maus.abstract.biz.id/health` 200, `zbmaus.abstract.biz.id/health` 200, `oc.niumination.id/health` 200, `ombrelay.abstract.biz.id/health` 200, `dsh.abstract.biz.id/health` 404
- `git log --oneline -1` → `45f54cb`; `git rev-list --count origin/main..HEAD` → 7
- `ls docs/registry` → 18 registry lives, termasuk `infrastructure-topology.md`, `dr-drill.md`, `vps-health-2026-11-20.md`

---

**Status:** audit selesai. Menunggu hasil probe VPS dari pemilik dan keputusan sebelum ada perubahan ekosistem.
