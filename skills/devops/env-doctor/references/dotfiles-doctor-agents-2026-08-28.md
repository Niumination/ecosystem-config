# Dotfiles `setup.sh --doctor` + `agents.zsh` — 2026-08-28

Dua kemampuan baru di `~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles` (repo sebelumnya bersih, main == origin/main @ `2b0c497`). Dirancang lewat brainstorming gate (desain di-approve user), diverifikasi dengan eksekusi nyata; commit+push tertunda persetujuan user.

## `setup.sh --doctor` — flag baru, 100% read-only

Cek berurutan (lapor ✅/⚠️/❌ per item; exit 1 kalau ada ❌):

| Seksi | Cek |
|---|---|
| Shell | login shell zsh (`dscl . -read $HOME UserShell`), `zsh -c 'source ~/.zshrc'` load test |
| Stow & symlinks | 11 path kunci: `.zshrc`, `.zshenv`, `.config/zsh/.zshrc`, `.config/zsh-abbr`, `.gitconfig`, `.fzf.zsh`, `.config/nvim`, `.config/tmux`, `.config/lazygit`, `kitty/kitty.conf`, `starship.toml` — symlink ke dalam repo = ✅, ke luar repo = ⚠️, real file = ⚠️, hilang = ❌ |
| Tools | 10 REQUIRED_TOOLS via `command -v`; `zsh -n` syntax untuk .zshrc / agents.zsh / aliases.zsh / functions.zsh |
| Git | `status --porcelain` (dirty) + `rev-list --left-right --count origin/main...HEAD` (ahead/behind dari ref lokal, tanpa fetch) |
| Agent & ecosystem | 5 config ada (`~/.hermes/.env`, `~/.9router/`, `vault/secrets.zsh`, `opencode.jsonc`, `~/.jcode/config.toml`) + `grep -il juan` residu check |

Hasil verifikasi aktual: **18 OK / 1 warn / 0 fail, exit 0** (1 warn = 5 file uncommitted, yaitu perubahan ini sendiri).

## `agents.zsh` — konsolidasi config agent shell

File baru `zsh/.config/zsh/agents.zsh`, di-source dari `.zshrc` setelah `docker.zsh`:

- **Dipindah persis tanpa ubah logika**: `ecosystem_root_guard()` + wrapper git/npm/npx/pnpm/yarn + `eco-check`/`eco-guard-status` (ex-`.zshrc` baris 81–153); wrapper `jcode()` (default opencode zen hy3-free) + `unset ANTHROPIC_API_KEY` (ex-`aliases.zsh` baris 7–21)
- **Baru**: `NUIMINATION_ROOT`, `HERMES_HOME` (dipindah dari .zshrc), alias `cc-at` → `services/cc-acehtengah`, abbr `jc`/`hr`/`eco` di `abbreviations.zsh`

Verifikasi: `whence -v ecosystem_root_guard` & `whence -v jcode` → "shell function from …/agents.zsh" ✅; guard pass di luar root (git di /tmp jalan normal) ✅; zsh load test bersih ✅. Catatan jujur: `abbr list` belum sempat diverifikasi (command kena approval-timeout) — jalankan `zsh -c 'source ~/.zshrc; abbr list' | grep eco` saat commit.

## Pitfall bash strict-mode (fix sudah masuk setup.sh)

1. `[[ -n "${3:-}" ]] && printf …` → kondisi false = exit code 1 = **ERR trap terpanggil** pada `set -Eeuo pipefail` + `trap … ERR`. Fix: `if [[ … ]]; then …; fi`.
2. `git rev-list --left-right --count origin/main...HEAD` → output `"0\t0"` **dipisah TAB**. Tanpa `tr '\t' ' '` dulu, `${counts%% *}` dan `${counts##* }` sama-sama menghasilkan `"0\t0"` (gejala: "ahead 0\t0 / behind 0\t0").

## HANDOFF — 5 file belum di-commit

```
 M setup.sh                               (+~150 baris: mode --doctor)
 M zsh/.zshrc                             (guard baris 81-153 → agents.zsh; +1 baris source)
 M zsh/.config/zsh/aliases.zsh            (jcode wrapper → agents.zsh)
 M zsh/.config/zsh-abbr/abbreviations.zsh (+3 abbr: jc, hr, eco)
?? zsh/.config/zsh/agents.zsh             (BARU)
```

Commit+push menunggu "gas/lanjut" dari user. Urutan saat dieksekusi:
1. Secret-check diff dulu: `git -C <repo> diff` + grep `sk-[a-zA-Z0-9]{20,}` (konvensi mass-repo-sync)
2. Commit: `feat(zsh): agents.zsh consolidation + setup.sh --doctor`
3. Push via https token — SSH publickey ditolak di mesin ini: `git push https://oauth2:${GH_TOKEN}@github.com/Niumination/zaryu-terminal-dotfiles.git main` (remote origin URL-nya SSH, tapi push tetap harus lewat https token)
4. Rerun `setup.sh --doctor` → semua check git harus hijau (dirty=0, ahead=0 setelah push)
