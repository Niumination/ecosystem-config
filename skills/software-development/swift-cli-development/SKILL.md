---
name: swift-cli-development
description: Swift CLI tools with SPM without Xcode.app — concurrency.
tags: [swift, spm, cli, concurrency, macos, argument-parser]
last_updated: "2026-09-04"
version: 1.0.0
---

# Swift CLI Development — SPM without Xcode

## Trigger
- User wants to build a Swift CLI tool
- Swift 6 concurrency errors (`@Sendable`, `@SendableClosureCaptures`, `#ActorIsolatedCall`, `#MutableGlobalVariable`)
- Storage-constrained macOS (Xcode.app not installed, <20GB free)
- Need to build Swift code without Xcode

## Context
Xcode.app requires ~12-15GB. On storage-constrained Macs, Swift CLI tools can be built with CommandLineTools + SPM directly. Swift 6 enforces strict concurrency checking by default, which causes build errors unfamiliar to developers coming from Swift 5 or other languages.

## Build Setup (No Xcode)

```bash
# Verify Swift is available (CommandLineTools includes Swift 6.x)
swift --version

# Build SPM package
cd Packages && swift build

# Build specific target
swift build --target <TargetName>

# Run executable
.build/debug/<executable-name> --help
```

## Swift 6 Concurrency Patterns

### Error: `capture of 'self' with non-Sendable type in @Sendable closure`
**Cause:** Capturing `self` in a closure that crosses actor boundaries.
**Fix:** Use `Task { @MainActor in }` or make the type `@unchecked Sendable`.

```swift
// ❌ Error
connection.stateUpdateHandler = { [weak self] state in
    self?.doSomething()  // DeviceDiscovery is not Sendable
}

// ✅ Fix 1: Task with MainActor
connection.stateUpdateHandler = { [weak self] state in
    Task { @MainActor in
        self?.doSomething()
    }
}

// ✅ Fix 2: Mark class as @unchecked Sendable
public class DeviceDiscovery: ObservableObject, @unchecked Sendable {
    // ...
}
```

### Error: `actor-isolated instance method cannot be called from outside of the actor`
**Cause:** Calling an actor method from non-actor context.
**Fix:** Wrap in `Task { await ... }`.

```swift
// ❌ Error
self?.handleConnection(connection)  // handleConnection is actor method

// ✅ Fix
Task {
    await self?.handleConnection(connection)
}
```

### Error: `actor-isolated property cannot be mutated from a Sendable closure`
**Cause:** Mutating actor state from callback.
**Fix:** Extract mutation into a non-isolated method called via Task.

```swift
// ❌ Error
self?.connections.removeAll { $0 === connection }

// ✅ Fix
Task {
    await self?.removeConnection(connection)
}

func removeConnection(_ connection: NWConnection) {
    connections.removeAll { $0 === connection }
}
```

### Error: `static property 'configuration' is not concurrency-safe`
**Cause:** ArgumentParser `CommandConfiguration` static property is global mutable state.
**Fix:** Mark the extension `@MainActor`.

```swift
// ❌ Error
extension NIUCastCommand {
    struct Mirror: AsyncParsableCommand {
        static var configuration = CommandConfiguration(...)
    }
}

// ✅ Fix
@MainActor
extension NIUCastCommand {
    struct Mirror: AsyncParsableCommand {
        static var configuration = CommandConfiguration(...)
    }
}
```

### Error: `sending 'self.adb' risks causing data races`
**Cause:** Struct property accessed across actor boundary.
**Fix:** Mark struct as `@unchecked Sendable`.

```swift
// ❌ Error
public struct ADBKit {
    public let adbPath: String
}

// ✅ Fix
public struct ADBKit: @unchecked Sendable {
    public let adbPath: String
}
```

### Error: `non-Sendable type of property cannot exit actor-isolated context`
**Cause:** Actor property used in non-isolated context.
**Fix:** Mark enum as `Sendable`.

```swift
// ❌ Error
public enum TCCPPort: Int { ... }

// ✅ Fix
public enum TCCPPort: Int, Sendable { ... }
```

### Error: `circular dependency between modules`
**Cause:** Two SPM targets import each other.
**Fix:** Restructure to remove cycle. Move shared types to a base module.

```swift
// ❌ Circular: ADBKit imports SharedModels, SharedModels imports ADBKit
.target(name: "ADBKit", dependencies: []),
.target(name: "SharedModels", dependencies: ["ADBKit"]),  // SharedModels can import ADBKit
```

## SPM Package Structure for CLI

```
Packages/
├── Package.swift
└── Sources/
    ├── ADBKit/              # Base library (no dependencies)
    │   └── ADBKit.swift
    ├── SharedModels/        # Shared types (depends on ADBKit)
    │   └── ADBDevice.swift
    ├── ScrcpyClient/        # Feature library
    │   └── ScrcpyClient.swift
    ├── NIUCastCLI/          # CLI command definitions
    │   ├── niu-cast.swift   # @main entry
    │   ├── DeviceCommand.swift
    │   ├── MirrorCommand.swift
    │   └── ...
    └── niu-cast-cli/        # Executable target
        └── main.swift       # Just calls NIUCastCommand.main()
```

**Key rules:**
- Executable target (`niu-cast-cli`) should only contain `main.swift` that calls the library's `main()`
- All command logic goes in the library target (`NIUCastCLI`)
- Base libraries (`ADBKit`, `SharedModels`) should have no SPM dependencies
- Feature libraries depend on base libraries, not on each other

## swift-argument-parser Patterns

```swift
import ArgumentParser

@main
struct NIUCastCommand: AsyncParsableCommand {
    static var configuration = CommandConfiguration(
        commandName: "niu-cast",
        abstract: "NIU CAST — Android Device Manager",
        version: "4.0.0",
        subcommands: [Device.self, Mirror.self, File.self],
        defaultSubcommand: Device.self
    )
}

@MainActor
extension NIUCastCommand {
    struct Mirror: AsyncParsableCommand {
        static var configuration = CommandConfiguration(
            commandName: "mirror",
            abstract: "Screen mirroring"
        )
        
        @Option(name: .shortAndLong, help: "Device serial")
        var serial: String?
        
        @Flag(name: .shortAndLong, help: "Stop mirroring")
        var stop = false
        
        mutating func run() async throws {
            // Command logic
        }
    }
}
```

**Important:** The `@MainActor` on the extension is required for Swift 6 concurrency safety with ArgumentParser.

## XcodeGen Without Xcode

`xcodegen` can generate `.xcodeproj` from `project.yml` without Xcode installed:

```bash
brew install xcodegen
xcodegen generate
# Creates niu-cast.xcodeproj — can be opened in Xcode later
```

This lets you write SwiftUI views now and build them later when Xcode is available.

## Storage-Constrained Workflow

When Xcode can't be installed (<20GB free):

1. **Write all code** — SwiftUI views, SPM packages, CLI commands
2. **Syntax check** — `swiftc -parse <file>` validates syntax without full build
3. **Build libraries** — `swift build --target <LibraryTarget>` builds SPM packages
4. **Build CLI** — `swift build --target niu-cast-cli` builds the executable
5. **Defer SwiftUI build** — SwiftUI views can't build without Xcode, but syntax is validated

```bash
# Syntax check all Swift files
for f in $(find . -name '*.swift'); do
    swiftc -parse "$f" 2>&1 | head -3
done
```

## Common Pitfalls

1. **Forgetting `@MainActor`** on ArgumentParser extensions → concurrency errors
2. **Circular dependencies** between SPM targets → build fails
3. **Actor isolation** in Network framework callbacks → use `Task { @MainActor in }`
4. **Non-Sendable types** crossing actor boundaries → mark as `@unchecked Sendable`
5. **Mutable global state** in ArgumentParser → `@MainActor` on extension

## Related
- `ecosystem-tool-adoption` — workflow for adopting external tools/repos (user-owned, recommend `hermes curator adopt ecosystem-tool-adoption`)
- `hermes-terminal-workflows` — terminal shell pitfalls
