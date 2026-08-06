# ODL-PDF (opendataloader-pdf) Setup Reference

## macOS Installation

### Java Setup (required)
```bash
# OpenJDK 26 installed via brew
brew install openjdk@21

# Java binary location
/usr/local/Cellar/openjdk/26.0.1/libexec/openjdk.jdk/Contents/Home/bin/java

# Symlink to ensure it's on PATH
ln -sf /usr/local/Cellar/openjdk/*/libexec/openjdk.jdk/Contents/Home/bin/java ~/.local/bin/java

# Set JAVA_HOME
export JAVA_HOME="/usr/local/Cellar/openjdk/*/libexec/openjdk.jdk/Contents/Home"
```

### Python Package Install
```bash
# Pip install fails due to easyocr → torch dependency on macOS
# Solution: install with --no-deps, then manually install deps except torch
pip install -e . --no-deps
pip install mss Pillow numpy pyautogui pynput pywinctl pyyaml python-dotenv scikit-image psutil websocket-client pydantic pyobjc-framework-Quartz
pip install "mcp>=1.0,<2" --no-build-isolation
```

Note: easyocr is skipped on macOS due to torch missing arm64 wheel for Python 3.14+. Fine — lazy import, only OCR path fails.

### Smoke Test
```bash
python3 -c "import opendataloader_pdf; print('OK')"
```

### Known Versions
- opendataloader-pdf: 2.5.0
- Java: OpenJDK 26.0.1 (Homebrew)
