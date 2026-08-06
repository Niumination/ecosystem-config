# Folder Rename Breaks Stow Symlinks

When a GNU Stow-managed dotfiles directory is renamed (e.g. `rekap/` → `dotfiles/`), all symlinks pointing into it become broken.

## Detection
```bash
find /Users/zaryu -maxdepth 5 -type l ! -exec test -e {} \; -ls 2>/dev/null
```

## Fix

### 1. Remove broken symlinks
```bash
find /Users/zaryu -maxdepth 5 -type l -lname "*rekap*" ! -exec test -e {} \; -delete
```

### 2. Re-stow from new location
```bash
cd /Users/zaryu/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles
stow --target="/Users/zaryu" zsh
stow --target="/Users/zaryu" nvim
stow --target="/Users/zaryu" starship
# ... etc for each package
```

### 3. Handle conflicts
```bash
# Remove non-stow files that block stow
rm -f /Users/zaryu/SHORTCUTS.md /Users/zaryu/.irbrc
stow --target="/Users/zaryu" nvim
```

## Verify
```bash
file ~/.zshrc ~/.gitconfig ~/.config/starship.toml
# Should say "Unicode text" or "ASCII text", not "broken symbolic link"
```
