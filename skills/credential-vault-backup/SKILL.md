---
name: credential-vault-backup
description: "Back up Niumination credentials into a single vault."
version: "1.0.0"
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [macos, linux]
tags: [credentials, vault, backup, security, niumination]
---

# Credential Vault Backup

Back up and centralize credentials from across the Niumination ecosystem into a single vault directory.

## Trigger

User asks to back up, consolidate, or inventory credentials across the ecosystem.

## Procedure

### 1. Identify credential sources

Scan for:
- `.env` files (exclude `.venv/`, `node_modules/`)
- `config.json`, `config.yaml`, `config.yml` (service configs)
- `auth.json`, `auth/` directories
- Files matching `*key*`, `*secret*`, `*token*`, `*credential*`
- SSH keys (`~/.ssh/`)
- Service-specific credential files (`~/.hermes/`, `~/.9router/`, `~/.antigravity/`)

### 2. Copy to vault

Target: `~/Desktop/Niumination/vault/`

```bash
cp ~/.hermes/.env ~/Desktop/Niumination/vault/hermes.env.bak
cp ~/.hermes/auth.json ~/Desktop/Niumination/vault/hermes-auth.json.bak
cp ~/.env.local ~/Desktop/Niumination/vault/home-env-local.bak
cp ~/.9router/auth/cli-secret ~/Desktop/Niumination/vault/9router-cli-secret.txt
cp ~/.9router/jwt-secret ~/Desktop/Niumination/vault/9router-jwt-secret.txt
cp ~/.9router/machine-id ~/Desktop/Niumination/vault/9router-machine-id.txt
cp ~/.9router/model-catalog-raw.json ~/Desktop/Niumination/vault/9router-model-catalog-raw.json
```

### 3. Set permissions

```bash
chmod 600 ~/Desktop/Niumination/vault/*.bak ~/Desktop/Niumination/vault/*.txt
```

### 4. Create/update README index

Maintain `README.md` in vault with:
- Table of all credential files and their sources
- Last update timestamp
- Access policy (chmod 600, no git commit)

### 5. Verify

```bash
ls -la ~/Desktop/Niumination/vault/
```

### 6. Rotate a stored secret (kredensial pengganti dari user)

1. **Backup dulu:** copy tiap file yang akan diubah ke `vault/_backup-credentials/<nama>.<YYYYMMDD>`.
2. **Taruh nilai baru di temp file vault** (`vault/.rot-<nama>.tmp`), bukan di teks perintah — lalu regex-replace tepat pada baris `VAR=...` di tiap file target, assert jumlah replacement ≥1 per file, dan hapus temp file segera.
3. **Cakup semua salinan var yang sama:** `secrets.zsh` (live, di-source shell), file `.bak` terkait, dan `~/.hermes/.env` bila menyimpan var itu (cek dulu dengan `grep -c` nama var saja).
4. **Verifikasi tanpa mencetak nilai:** assert string cocok di semua file (cetak `COCOK/BEDA` saja), `chmod 600`, pastikan `git status` vault clean (vault wajib git-ignored).
5. **Lapor:** nama file + jumlah replacement + hasil uji key bila diminta — tidak pernah nilainya.
6. **Key provider baru:** pakai pola file khusus `vault/<provider>-key.md` (seperti `github-pat.md`, `explabs-key.md`) berisi env var, nilai (aman — dalam vault), dan catatan status uji (model mana yang lolos probe); tambah baris indeks di `vault/README.md`.

## Pitfalls

- **Never commit vault to git.** The vault directory must be in `.gitignore` of all repos. Credentials in vault are for local backup only.
- **chmod 600 for all sensitive files.** World-readable credentials are a security risk. Verify with `ls -la` after copy.
- **Exclude runtime files.** Don't copy databases (`*.db`, `*.sqlite`), logs (`*.log`), or `__pycache__/`. These are not credentials and may be large.
- **Use `git add -f` for ignored files.** When a file is git-ignored but should be tracked (like a config template), use `git add -f` to override.
- **Don't echo secrets to chat.** When reporting, show file names and metadata only. Never print API keys, tokens, or passwords in conversation.
- **Never pass secret values in command text.** Terminal commands persist in output caches/logs — a key inside `export FOO=...` or an inline script is a write to log. Hand a new secret to scripts via a temp file inside the git-ignored vault, read it programmatically, delete immediately after.

## Verification

```bash
# Check vault contents
ls -la ~/Desktop/Niumination/vault/

# Verify permissions (should be -rw-------)
find ~/Desktop/Niumination/vault -type f ! -name ".DS_Store" -exec ls -la {} \;
```
