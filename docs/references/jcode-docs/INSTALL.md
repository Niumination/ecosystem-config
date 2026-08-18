# Instalasi jcode

## Metode yang Digunakan: Homebrew

```bash
# 1. Tambah tap repository
brew tap 1jehuang/jcode

# 2. Install
brew install jcode
```

**Output instalasi:**
```
Tapped 1 formula (14 files, 40.2KB).
Installing jcode from 1jehuang/jcode...
/usr/local/Cellar/jcode/0.12.2: 4 files, 75.4MB, built in 2 seconds
```

## Provider Setup: OpenRouter (Gratis)

### 1. Set API Key
Tambahkan ke `~/.config/zsh/01-environment.zsh`:
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### 2. Set Default Provider & Model
Edit `~/.jcode/config.toml`:
```toml
[provider]
default_provider = "openrouter"
default_model = "z-ai/glm-4.5-air:free"
```

### 3. Smoke Test
```bash
jcode run "say hello"
# Hello! How can I help you today?
```

### Model Gratis Tersedia di OpenRouter
| Model ID | Nama | Keterangan |
|----------|------|------------|
| `z-ai/glm-4.5-air:free` | GLM 4.5 Air | ✅ Aktif digunakan |
| `qwen/qwen3-coder:free` | Qwen3 Coder 480B | Bagus untuk coding, kadang rate-limited |
| `deepseek/deepseek-v4-flash:free` | DeepSeek V4 Flash | Kualitas rendah |
| `minimax/minimax-m2.5:free` | MiniMax M2.5 | Alternatif |
| `google/gemma-4-31b-it:free` | Google Gemma 4 31B | Alternatif |
| `openai/gpt-oss-120b:free` | GPT-OSS 120B | Alternatif |

Semua model `:free` **tidak consume credits** OpenRouter.

## Verifikasi

```bash
jcode --version
# jcode v0.12.2 (4f37cae4)
```

## Metode Alternatif

### Install Script (macOS & Linux)
```bash
curl -fsSL https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.sh | bash
```

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.ps1 | iex
```

### Build dari Source
```bash
# Install Rust terlebih dahulu
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone dan build
git clone https://github.com/1jehuang/jcode.git
cd jcode
cargo build --release

# Install ke PATH
scripts/install_release.sh
```

## Platform Support

| Platform | Status |
|----------|--------|
| Linux x86_64 / aarch64 | Fully supported |
| macOS Apple Silicon & Intel | Supported |
| Windows x86_64 | Supported (native + WSL2) |

## Update

```bash
brew update && brew upgrade jcode
```

## Uninstall

```bash
brew uninstall jcode
brew untap 1jehuang/jcode

# Hapus config (opsional)
rm -rf ~/.jcode/
```

## Telemetry Opt-out

jcode mengirim data penggunaan anonim (install count, versi, OS, aktivitas sesi, tool counts, crash/exit reasons). **Tidak ada** kode, nama file, prompt, atau data pribadi yang dikirim.

Untuk menonaktifkan, tambahkan ke shell profile (`~/.config/zsh/01-environment.zsh`):

```bash
export JCODE_NO_TELEMETRY=1
```

Kemudian reload:
```bash
source ~/.config/zsh/01-environment.zsh
```
