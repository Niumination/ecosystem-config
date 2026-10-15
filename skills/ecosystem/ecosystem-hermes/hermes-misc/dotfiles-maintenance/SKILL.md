---
name: dotfiles-maintenance
description: Use when developing or fixing zaryu-terminal-dotfiles.
tags: [dotfiles, stow, zsh, brew, ci, niumination]
version: 1.0.0
author: Hermes Agent (Niumination)
license: MIT
metadata:
  hermes:
    tags: [dotfiles, stow, zsh, brew, ci, niumination]
    related_skills: [env-doctor, up-eco, brainstorming]
---

# Dotfiles Maintenance — zaryu-terminal-dotfiles

## When to Use

- User minta cek/kembangkan/fix dotfiles, setup.sh, paket stow, Brewfile, atau CI repo ini
- Pasca-insiden env (stow broken, zsh error) — kombinasikan dengan `env-doctor`
- Setup Mac baru dengan repo ini

Repo: `~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles` (remote `Niumination/zaryu-terminal-dotfiles`, private). GNU Stow, 17 paket, setup.sh idempotent.

## Alat bawaan repo (pakai ini, jangan reinvent)

| Perintah | Fungsi |
|---|---|
| `bash setup.sh --doctor` | Health check read-only: shell, stow symlinks (11), tools, syntax zsh, git repo, config agent + residu juan-router. Exit 1 jika gagal. |
| `bash setup.sh --bootstrap` | Mac baru: install Homebrew (non-interaktif) + `brew bundle install` + stow. Idempotent. |
| `bash setup.sh --dry-run` | Preview stow tanpa perubahan. |
| `zsh -c 'source ~/.zshrc && echo OK'` | Load test zsh — WAJIB pakai zsh, bukan bash. |

## Struktur penting

- `zsh/.config/zsh/agents.zsh` — konsolidasi agent/ecosistem: jcode wrapper (default opencode zen hy3-free), `ecosystem_root_guard()` + wrapper git/npm/npx/pnpm/yarn, `HERMES_HOME`, `NUIMINATION_ROOT`, alias `cc-at`, abbr `jc`/`hr`/`eco`.
- `.zshrc` hanya entry point — source modular: plugins, aliases, functions, colors, docker, agents (urutan ini).
- `shared/environment.sh` — env vars global (DOTFILES_DIR fallback, XDG, FZF).
- `.github/workflows/ci.yml` — CI: shellcheck (setup.sh + bin/ skip non-shebang binary) + `zsh -n` 9 file + smoke `--help`, runner ubuntu-latest.
- `git/.gitconfig` — punya `[url "https://github.com/"] insteadOf = git@github.com:` (SSH rusak di mesin ini) + credential.helper osxkeychain.

## Workflow pengembangan (terbukti 28-Agu-2026)

1. **Eksplorasi dulu**: baca README.md (817 baris, ada tabel packages + changelog), setup.sh, file target sebelum edit.
2. **Desain → approve → eksekusi** (brainstorming HARD GATE berlaku untuk fitur baru).
3. **Verifikasi lokal SEBELUM push** (CI harus dijamin hijau):
   - `shellcheck -S warning setup.sh` + semua script ber-shebang di `bin/.local/bin/` (SKIP file tanpa shebang seperti `xurl` = binary Go — JANGAN pakai `file` untuk deteksi, di macOS semua executable disebut "executable").
   - `zsh -n` untuk semua file zsh.
   - `bash setup.sh --doctor` → harus 0 gagal.
4. **Commit format**: `type(scope): pesan` (feat/fix/docs/ci) — konsisten dengan riwayat repo.
5. **Push**: `git push` biasa jalan (insteadOf + keychain).
6. **Pantau CI sampai hijau** — API: `curl -H "Authorization: token $GH_TOKEN" "https://api.github.com/repos/Niumination/zaryu-terminal-dotfiles/actions/runs?head_sha=<sha>"` (GH_TOKEN dari `vault/secrets.zsh`). Loop poll ~10s hingga `completed`.

## Pitfalls

- **Push file `.github/workflows/`** butuh PAT scope `workflow`. Token keychain lama TIDAK punya scope itu → gunakan `git push https://oauth2:${GH_TOKEN}@github.com/...` dengan GH_TOKEN dari vault. Token vault = PAT no-expiry repo+workflow.
- **shellcheck versi CI (ubuntu apt 0.9.0) ≠ lokal (brew 0.11.0)** — lokal bisa lolos tapi CI gagal (kasus SC2155). Selalu jalankan shellcheck lokal TAPI tetap pantau run CI pertama.
- **SC2155**: pisah `local x="$(cmd)"` jadi `local x; x="$(cmd)"`.
- **Brewfile**: JANGAN tambah `tap "homebrew/bundle"` / `tap "homebrew/services"` — deprecated (kosong) sejak Homebrew v6, membuat `brew bundle check` selalu gagal.
- **Circular dependency libtiff/webp** = stale keg tabs; fix `brew update` lalu retry bundle.
- **Keychain update via agent bisa terblokir approval** — kalau 2x timeout, minta user jalankan manual: `security add-internet-password -U -a oauth2 -s github.com -r htps -w <token>` (tanpa `-a oauth2` akan gagal usage error).
- **State zsh (.zsh_history, .zsh_sessions, .zcompdump)** nulis masuk direktori repo via symlink stow — sudah di-.gitignore, bukan bug; jangan "perbaiki" kecuali diminta.
- **README 817 baris** — patch section spesifik (tabel packages, fitur setup.sh, changelog di bawah), jangan rewrite.

## Checklist pasca-edit

- [ ] `shellcheck -S warning` bersih (setup.sh + bin scripts)
- [ ] `zsh -n` bersih semua file zsh
- [ ] `bash setup.sh --doctor` → 0 gagal
- [ ] Commit + push
- [ ] CI hijau (poll API)
- [ ] Update changelog README.md jika fitur baru
- [ ] Update changelog ekosistem `brain/docs/ecosystem-changelog.md` jika perubahan signifikan
