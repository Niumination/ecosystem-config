# Storage-Constrained macOS Development

> Pattern for developing Swift apps without Xcode.app (15GB+ required)  
> Discovered during niu-cast v4.0 development (4-Sep-2026)

---

## Problem

Xcode.app requires ~12-15GB storage. Many Macs (especially base models with 128-256GB) don't have enough free space. But Swift development is still possible.

## Solution: SPM + CommandLineTools

Swift 6.x ships with CommandLineTools (no Xcode needed). SPM (Swift Package Manager) can build libraries and CLI tools directly.

### What works without Xcode
- ✅ SPM libraries (`.target`)
- ✅ CLI tools (`swift-argument-parser`)
- ✅ `xcodegen` → generates `.xcodeproj` for later
- ✅ Syntax checking (`swiftc -parse`)
- ✅ Unit tests (`swift test`)

### What doesn't work without Xcode
- ❌ SwiftUI app targets (need Xcode's `xcodebuild`)
- ❌ macOS app bundles
- ❌ iOS/watchOS/tvOS targets
- ❌ Interface Builder / Storyboards
- ❌ Instruments profiling

## Workflow

### 1. Write all code now
Write SwiftUI views, SPM packages, CLI commands — all of it. Syntax is validated with `swiftc -parse`.

### 2. Build libraries and CLI
```bash
cd Packages
swift build                    # Build everything
swift build --target MyLib     # Build specific library
swift build --target my-cli    # Build CLI executable
```

### 3. Defer SwiftUI build
SwiftUI views can't build without Xcode, but syntax is validated. Build them later when:
- External SSD is available for Xcode
- CI/CD builds the app
- Machine is upgraded

### 4. Use XcodeGen for project generation
```bash
brew install xcodegen
xcodegen generate              # Creates .xcodeproj from project.yml
```
The `.xcodeproj` can be opened in Xcode later — no re-generation needed.

## Real-World Example: niu-cast v4.0

**Machine:** macOS 128GB, 15GB free  
**Goal:** Android screen mirroring app (Swift rewrite of Python v3.7)

**Approach:**
1. Wrote 6 SPM packages (ADBKit, ScrcpyClient, MirrorEngine, FusionEngine, DeviceDiscovery, TCCPKit)
2. Wrote 5 CLI commands (device, mirror, file, qr, server)
3. Wrote SwiftUI views (MainView, MirrorWindow, FilesWindow, PairingSheet)
4. All syntax-validated with `swiftc -parse`
5. Libraries build successfully with `swift build`
6. CLI builds successfully
7. SwiftUI views deferred until Xcode is available

**Result:** 19 Swift files, 5 commits, full architecture in place — zero Xcode usage.

## Alternatives to Xcode

| Tool | Storage | Purpose |
|------|---------|---------|
| SPM (built-in) | 0 bytes | Build libraries & CLI |
| `xcodegen` | ~50MB | Generate `.xcodeproj` |
| VS Code + Swift extension | ~300MB | Code editing |
| `swiftc -parse` | 0 bytes | Syntax check |

## When to Use This Pattern

- Machine has <20GB free
- Building CLI tools or libraries
- Writing SwiftUI for later build
- CI/CD will handle final app build
- External SSD available for occasional Xcode use

## Related
- `swift-cli-development` skill — Swift 6 concurrency patterns
- `ecosystem-tool-adoption` skill — adopting external tools/repos
