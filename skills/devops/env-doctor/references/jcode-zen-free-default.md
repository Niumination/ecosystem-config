# JCode + OpenCode Zen — Clean, Reconfigure & Free-Tier Default

Captures the 2026-08-28 clean & reconfigure flow that made `jcode run` and `opencode run` work without `--provider`/`--model` (user: "Gunakan opencode zen sebagai default, pilih model free tier").

## Backup & Clean

```bash
TS=$(date +%Y%m%d%H%M%S); mkdir -p ~/Backups/config-clean-$TS
cp -R ~/.config/opencode ~/Backups/config-clean-$TS/opencode.config
cp -R ~/.jcode ~/Backups/config-clean-$TS/jcode
cp -R ~/.local/share/opencode ~/Backups/config-clean-$TS/opencode.share
cp ~/.hermes/.env ~/Backups/config-clean-$TS/hermes.env

rm -f ~/.local/share/opencode/auth.json ~/.config/opencode/opencode.jsonc
rm -f ~/.config/jcode/opencode*.env; rm -rf ~/.jcode/cache/*
# keep ~/.jcode/config.toml — healthy (219 lines)
```

## Recreate with Free Tier (no billing)

`opencode.jsonc` minimal with default model avoids `CreditsError: No payment method` on workspace `wrk_01KRR4R9YNHVJ349SQD0P6JKFM`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/hy3-free"
}
```

Auth from canonical `~/.hermes/.env` (OPENCODE_ZEN_API_KEY, OPENCODE_GO_API_KEY):

```bash
source ~/.hermes/.env
export OPENCODE_ZEN_API_KEY=$(grep OPENCODE_ZEN_API_KEY ~/.hermes/.env | cut -d= -f2 | tr -d '"')
mkdir -p ~/.local/share/opencode
cat > ~/.local/share/opencode/auth.json <<EOF
{ "opencode": { "type": "api", "key": "$OPENCODE_ZEN_API_KEY" } }
EOF
mkdir -p ~/.config/jcode
echo "OPENCODE_API_KEY=$OPENCODE_ZEN_API_KEY" > ~/.config/jcode/opencode.env
echo "OPENCODE_GO_API_KEY=$OPENCODE_GO_API_KEY" > ~/.config/jcode/opencode-go.env
```

## Model mapping (jcode --provider opencode)

`jcode model list --provider opencode` shows both paid and free. Bare names for jcode (no `opencode/` prefix):

- `hy3-free` ✅ PONG (proven)
- `laguna-s-2.1-free` ✅ PONG
- `nemotron-3-ultra-free` → 502 overloaded (retryable, free but flaky)
- `muse-spark-1.2-contributor-free` via jcode → ModelError not supported (use via `opencode` CLI only)
- `claude-opus-5`, `gpt-5-nano`, etc via zen without payment → `CreditsError: No payment method`

Always test with `timeout 20 jcode run --provider opencode --model <bare> "say PONG"`.

## Default wrapper (no native config.toml default_model)

jcode `config.toml` has no `[provider]`/`[providers]` default_model. Add shell wrapper in `~/zsh/.config/zsh/aliases.zsh` so `jcode run "hello"` auto-injects:

```zsh
jcode() {
  if [[ "$1" == "run" ]]; then
    local has_provider=false
    for arg in "$@"; do [[ "$arg" == "--provider" || "$arg" == "-p" ]] && has_provider=true; done
    if [[ "$has_provider" == false ]]; then
      command jcode --provider opencode --model hy3-free "$@"; return
    fi
  fi
  command jcode "$@"
}
```

Verify only under zsh: `zsh -c 'source ~/.zshrc && jcode run "say PONG"'`. Explicit `--provider`/`--model` bypasses wrapper.

## Dotfiles sync without bloat

HOME is the stow dir (`.git -> Desktop/.../.git`), so `git status` in repo shows many `AD` from HOME. Never `git add .`:

```bash
cp ~/zsh/.config/zsh/aliases.zsh ~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/zsh/.config/zsh/aliases.zsh
cd ~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles
git diff -- zsh/.config/zsh/aliases.zsh
git add zsh/.config/zsh/aliases.zsh
# if prior commit staged bloat: git reset --soft HEAD~1; git restore --staged .; git add <file>
git commit -m "feat(zsh): jcode default wrapper -> opencode zen hy3-free"
```

Push fallback when SSH `Permission denied (publickey)` / `Host key verification failed`:

```bash
source ~/.hermes/.env
git remote set-url origin "https://oauth2:${GITHUB_TOKEN}@github.com/Niumination/zaryu-terminal-dotfiles.git"
git push
git remote set-url origin git@github.com:Niumination/zaryu-terminal-dotfiles.git
```
