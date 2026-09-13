# Swift 6 Concurrency Errors — Reference

> Errors encountered during niu-cast v4.0 development (4-Sep-2026)  
> Swift 6.3.2, CommandLineTools (no Xcode.app), SPM build

---

## Error Catalog

### 1. `@SendableClosureCaptures`
**Full message:** `capture of 'self' with non-Sendable type 'DeviceDiscovery?' in a '@Sendable' closure`

**Context:** Network framework's `NWConnection.stateUpdateHandler` is `@Sendable`, so capturing `self` (a non-Sendable class) is an error.

**Fix pattern:**
```swift
// ❌
connection.stateUpdateHandler = { [weak self] state in
    self?.doSomething()
}

// ✅
connection.stateUpdateHandler = { [weak self] state in
    Task { @MainActor in
        self?.doSomething()
    }
}
```

**Also applies to:** `NWListener.newConnectionHandler`, `NWBrowser.browseResultsChangedHandler`

### 2. `#ActorIsolatedCall`
**Full message:** `call to actor-isolated instance method 'handleConnection' in a synchronous nonisolated context`

**Context:** Actor methods can't be called directly from non-actor closures.

**Fix pattern:**
```swift
// ❌
listener?.newConnectionHandler = { [weak self] connection in
    self?.handleConnection(connection)
}

// ✅
listener?.newConnectionHandler = { [weak self] connection in
    Task {
        await self?.handleConnection(connection)
    }
}
```

### 3. `#MutableGlobalVariable`
**Full message:** `static property 'configuration' is not concurrency-safe because it is nonisolated global shared mutable state`

**Context:** ArgumentParser's `CommandConfiguration` is a static property that's implicitly mutable.

**Fix pattern:**
```swift
// ❌
extension NIUCastCommand {
    struct Mirror: AsyncParsableCommand {
        static var configuration = CommandConfiguration(...)
    }
}

// ✅
@MainActor
extension NIUCastCommand {
    struct Mirror: AsyncParsableCommand {
        static var configuration = CommandConfiguration(...)
    }
}
```

### 4. `#SendingRisksDataRace`
**Full message:** `sending 'self.adb' risks causing data races`

**Context:** Struct property accessed across actor boundary.

**Fix pattern:**
```swift
// ❌
public struct ADBKit {
    public let adbPath: String
}

// ✅
public struct ADBKit: @unchecked Sendable {
    public let adbPath: String
}
```

### 5. Non-Sendable property exiting actor-isolated context
**Full message:** `non-Sendable type 'TCCPPort' of property 'port' cannot exit actor-isolated context`

**Context:** Actor property used in non-isolated context.

**Fix pattern:**
```swift
// ❌
public enum TCCPPort: Int { ... }

// ✅
public enum TCCPPort: Int, Sendable { ... }
```

### 6. Circular dependency between modules
**Full message:** `circular dependency between modules 'SharedModels' and 'ADBKit'`

**Context:** Two SPM targets import each other.

**Fix:** Restructure dependencies to be unidirectional. Move shared types to a base module.

```swift
// ❌
.target(name: "ADBKit", dependencies: ["SharedModels"]),
.target(name: "SharedModels", dependencies: ["ADBKit"]),

// ✅
.target(name: "ADBKit", dependencies: []),
.target(name: "SharedModels", dependencies: ["ADBKit"]),
```

### 7. Failable initializer cannot override non-failable
**Full message:** `failable initializer 'init()' cannot override a non-failable initializer`

**Context:** `MTKViewDelegate` requires non-failable `init()`.

**Fix pattern:**
```swift
// ❌
public class MirrorEngine: NSObject, MTKViewDelegate {
    public init?() { ... }
}

// ✅
public class MirrorEngine: NSObject {
    public override init() { ... }
}
```

---

## Swift 6 Concurrency Cheat Sheet

| Type | Mark as | When |
|------|---------|------|
| Struct used across actors | `@unchecked Sendable` | Struct has only `let` properties |
| Enum used across actors | `Sendable` | Enum has no associated values or all are Sendable |
| Class with mutable state | `@unchecked Sendable` | Class is only accessed from MainActor |
| Actor method from closure | `Task { await ... }` | Any non-actor closure |
| Actor property mutation | Extract to non-isolated method | From Sendable closure |
| ArgumentParser extension | `@MainActor` | Always |
| Network framework callback | `Task { @MainActor in }` | `NWConnection`, `NWListener`, `NWBrowser` |

---

## Build Commands

```bash
# Syntax check (no build artifacts)
swiftc -parse File.swift

# Build SPM package
cd Packages && swift build

# Build specific target
swift build --target niu-cast-cli

# Run executable
.build/debug/niu-cast --help
```

---

## Related
- Swift 6 Migration Guide: https://www.swift.org/migration/documentation/
- `ecosystem-tool-adoption` skill — workflow for adopting external tools/repos
