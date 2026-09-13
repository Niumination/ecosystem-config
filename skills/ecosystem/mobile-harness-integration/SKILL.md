---
name: mobile-harness-integration
description: Add new agent runtimes to Mobile-Harness Android app.
tags:
  - mobile
  - android
  - hermes
  - runtime
  - agent-integration
last_updated: "2026-09-13"
version: 3.4.12
changes:
  - v3.4.12: ViewModel event-gate rule (isRunning/activeSessionId silent drops)
changes:
  - v3.4.11: hybrid guest install (pinned checkout + uv sync, tarball demoted to fallback), post-exit output reconcile rule
changes:
  - v3.4.9: event-collector wiring rule (uncollected SharedFlow = dead UI), toast denylist over allowlist
  - v3.4.10: shell-dollar idiom + missing-backslash verification
changes:
  - v3.4.8: probe-vs-execution-path rule, spawn output-file race, unmappable-option rule, one-shot-chat memory rule, speculative-transcript rule
changes:
  - v3.4.7: guest package-source staleness rule (pinned tarball over stale registry), update-path coverage rule, blank-HOME env-leak clause, escape-copy verification rule
  - v3.4.6: blank-HOME host reproduction pitfall for guest CLI failures
  - v3.4.5: enum pitfall gains fixed-count test assertions
  - v3.4.4: quirks ref gains official per-family endpoint table; UI-gate pitfall (gate on provider kind, not agent)
  - v3.4.3: quirks ref gains Zen /v1 base-path rule + public models-list enumeration
  - v3.4.2: dev-stack pip-vs-interpreter clause; ps-ARGS live-install probe
  - v3.4.1: fixed-tag release asset verification via updatedAt
  - v3.4.0: corrected Hermes runtime section to real CLI surface
  - v3.3.0: on-device ADB test loop section; opencode-endpoint-quirks reference (Zen free-tier lock, Go session header)
changes:
  - v3.2.0: validation echoes server error bodies; key-free endpoint probe; OAuth agents skip provider step; CI ephemeral-signature note
  - v3.0.0: Added CI/CD build APK workflow, Play Protect signing requirements, deepseek_harness merge conflict resolution details, documentation requirements
  - v2.0.0: Added deepseek_harness merge strategy, Hermes-specific integration details, conflict resolution patterns, documentation requirements
  - v1.0.0: Initial release
---

# Mobile-Harness Runtime Integration

## Trigger
Adding a new agent runtime to the Android app. Extending Mobile-Harness with new agent support. Modifying `app/src/main/java/com/jarves/mh/` files.

## Architecture Pattern

Mobile-Harness runs agent CLIs inside a private Termux/Linux runtime on Android.
Each agent has:
1. An `AgentKind` enum entry in `Models.kt`
2. A `RuntimeBridge` implementation class
3. An entry in `AgentRegistry.builtIns()` in `AgentDriver.kt`
4. An installation method in `RuntimeInstaller.kt`
5. UI color + abbreviation in `PocketDevApp.kt`

## Workflow: Adding a New Agent Runtime

### Step 0: Merge multi-agent infrastructure (if needed)

If the `main` branch lacks multi-agent infrastructure, merge `remotes/origin/deepseek_harness` first:

```bash
git fetch origin
git merge remotes/origin/deepseek_harness
```

**Why merge deepseek_harness instead of building from scratch on main?**
The `deepseek_harness` branch contains the complete multi-agent infrastructure that `main` lacks. Building from scratch on main would require writing `AgentDriver`, `AgentRegistry`, `RuntimeInstaller`, `NativeSpawnProcess`, and `MainViewModel` orchestration from zero. Merging inherits all of this proven infrastructure.

**Conflict resolution pattern (from actual merge):**
- `Models.kt`: Use deepseek branch as base (has AgentKind + ProviderKind), then add back Niumination providers (AGENTROUTER, HUANCHENG, NINE_ROUTER) and the new agent.
- `PocketDevApp.kt`: Use deepseek branch as base, add back ALL provider color/mark entries from HEAD, add new agent entries.
- **Never use deepseek's ProviderKind list as-is** — it removed providers Niumination needs (AGENTROUTER, HUANCHENG, NINE_ROUTER)
- Always verify: `grep -rn '<<<<<<<' app/` → 0 results.

The `deepseek_harness` branch provides the essential infrastructure:
- `AgentDriver.kt` with `AgentRegistry.builtIns()` pattern
- `RuntimeBridge.kt` with extended interface
- `RuntimeInstaller.kt` with multi-agent `ensureAgentInstalled()`
- `MainViewModel.kt` with `AgentRegistry` orchestration
- `NativeSpawnProcess.kt` with process management

### Step 1: Add AgentKind enum entry
In `app/src/main/java/com/jarves/mh/model/Models.kt`:
```kotlin
enum class AgentKind(
    val stableId: String,
    val title: String,
    val subtitle: String,
    val downloadNote: String,
) {
    NEW_AGENT("new-agent-id", "Display Name", "Description", "Size"),
    ;
}
```
Also add to `providersForAgent()` function and provider constants. Add `HERMES_PROVIDERS` or equivalent set for the new agent's compatible providers.

### Step 2: Create RuntimeBridge implementation
Create `app/src/main/java/com/jarves/mh/runtime/<Name>RuntimeBridge.kt`:
- Extend `RuntimeBridge` interface
- Implement `startSession()`, `stopSession()`, `respondToApproval()`, etc.
- Spawn through `installer.process(...)` (proot) and stream the guest process stdout — verify every CLI flag and env var against the tool's own live docs/skill BEFORE encoding it; assumed flags (`--prompt`, `--project`, `--api-url`) compile fine and fail only on-device, silently.
- Emit `RuntimeEvent` for the UI; every failure path must surface the tool's stderr tail, never a static message.
- Reproduce a guest CLI failure on the host with a blank HOME before blaming the device — `HOME=$(mktemp -d) <cli> <same flags>` separates first-run bootstrap problems (missing config/auth init) from on-device spawn problems; a clean-HOME success on host with instant death on device means the spawn path, not the tool, is broken. A blank HOME alone is NOT sufficient isolation: exported config env vars (e.g. `HERMES_HOME`) bypass HOME entirely and leak the real config into the 'clean' run, producing a false success — list the tool's config env vars first and unset them for the repro, or the comparison proves nothing.
- **Communication protocol**: Most agents use stdin/stdout JSON-RPC via `ProcessBuilder`. Set environment variables for provider configuration.
- For Python-based agents (like Hermes): invoke via `pip install` then `hermes chat --prompt <text>`

### Step 3: Register in AgentDriver
In `app/src/main/java/com/jarves/mh/runtime/AgentDriver.kt`:
- Add import for the new bridge
- Add parameter to `AgentRegistry.builtIns()` — **NOTE: adding a new parameter changes the signature, breaking all call sites**
- Add `BuiltInAgentDriver(NEW_AGENT, bridge, capabilities)` entry

### Step 4: Add installation logic
In `app/src/main/java/com/jarves/mh/runtime/RuntimeInstaller.kt`:
- Add `ensure<Name>Installed()` method
- Add `AgentKind.NEW_AGENT -> ensure<Name>Installed(...)` in `ensureAgentInstalled()`
- Add `AgentKind.NEW_AGENT -> isInstalled() && ...` in `isAgentInstalled()`
- Write version marker file after installation
- Add version property (e.g., `val hermesVersion: String get() = hermesMarker.readTextOrNull().orEmpty()`)
- Register the marker in `installedAgentVersions()` (same file) or Settings never shows the agent as installed — marker file + version property alone are invisible to the UI
- Markers get lost while binaries survive (backup restore, installer re-run that never finished): add a self-heal path that runs `<tool> --version` inside the guest and rewrites the marker from the parsed output when the binary is healthy but the marker is blank. Gate it strictly — binary-unusable means reinstall, never marker fabrication.

### Step 5: Add UI entry
In `app/src/main/java/com/jarves/mh/ui/PocketDevApp.kt`:
- Add `AgentKind.NEW_AGENT -> Color(...)` to the color map
- Add `AgentKind.NEW_AGENT -> "XX"` to the abbreviation map
- Color mapping for `ProviderKind` entries too (same pattern)

### Step 6: Update MainViewModel
In `app/src/main/java/com/jarves/mh/ui/MainViewModel.kt`:
- Add import for the new bridge
- Add `private val <name>Runtime = <Name>RuntimeBridge(application) { profile -> vault.get(profile.kind.name) }`
- Update `AgentRegistry.builtIns(...)` to include `<name>Runtime`
- Collect its events next to the existing collectors: `viewModelScope.launch { <name>Runtime.events.collect(::onRuntimeEvent) }`. A `SharedFlow(replay=0)` with no collector drops every event silently — sessions run, answers never render, `isRunning` never clears, no failure ever toasts, and the app reads as 'connected but no response'. Symbol-presence greps pass while the wiring is missing, so assert the `collect` line itself (see Verification), never just the bridge reference.

### Step 7: Update manifest and README
- Add agent to `README.md` coding agents table
- Add agent to Runtime Components section
- Update "Current Limitations" if agent has specific constraints

### Step 8: Add documentation
Create `docs/HERMES-AGENT-INTEGRATION.md` (or `<AGENT>-INTEGRATION.md`) and update `docs/DEVELOPMENT-GUIDE.md`. Add `AGENTS.md` to the project root.

## How Hermes Agent Runs on Android

Hermes Agent (by Nous Research, `pip install hermes-agent`) runs inside the PRoot Linux guest. The bridge MUST use the real CLI surface (verified against the hermes-agent skill's cli-reference, never assumed):

```bash
hermes chat -q "PROMPT" -Q -m MODEL --provider NAME   # one-shot, quiet, final response on stdout
```

- Spawn via `installer.process(proot, rootfs, workspace, env, cmd)` — the same proot mechanism the DeepSeek bridge uses. Never `ProcessBuilder` on Android: the guest binary is not on the Android PATH, direct start always throws, and a bridge that swallows that into `null` hangs the UI at "Think" forever with zero diagnostics.
- Provider selection uses Hermes' BUILT-IN provider names (`opencode-go`, `opencode-zen`, `anthropic`, `openai`, `deepseek`, `gemini`, `xai`, `openrouter`) chosen by matching the configured base URL; secrets travel as the provider's key env var (`OPENCODE_GO_API_KEY`, …). Endpoints with no built-in mapping must fail LOUDLY, never silently.
- `-Q` output is plain text, not JSON events — stream lines as they arrive and fail loudly with the tail on non-zero exit.

### Communication Protocol
- PRoot spawn via `RuntimeInstaller.process`, stdout streamed line-by-line as plain text (Hermes one-shot mode), NOT stdin/stdout JSON-RPC.
- Provider config = CLI flags (`-m`, `--provider`) + key env vars; Hermes reads settings from its own config, secrets from env.

### Environment Variables
Hermes reads settings from its own config and secrets from env — only the provider's key env var is passed (`OPENCODE_GO_API_KEY`, `OPENCODE_ZEN_API_KEY`, `ANTHROPIC_API_KEY`, …). Do NOT invent `*_BASE_URL` / `*_MODEL` env vars; the CLI does not read them.

`ProviderProfile` carries no `authToken` field — the bridge receives a `secretFor` lambda backed by `ApiKeyVault`, keyed by `ProviderKind`.

### Supported Providers
`HERMES_PROVIDERS` in `Models.kt` is the curated onboarding set — real endpoints only, no localhost presets (owner decision after device testing showed `http://localhost` resolves to the phone itself, never a Mac-side router):
- **Anthropic API** (`ANTHROPIC`) — usage-billed Console key
- **OpenCode Zen** (`OPENCODE_ZEN`) — fixed `OPENAI_RESPONSES` entry
- **OpenCode Free** (`OPENCODE_FREE`) — keyless preset, fixed `OPENAI_CHAT` entry, no key field
- **OpenCode Go** (`opencode-go` via custom base `https://opencode.ai/zen/go/v1`) — Hermes built-in provider name, session header required
- **Custom** (`CUSTOM`) — user endpoint, wire protocol chosen in onboarding

## Merge Conflicts (from deepseek_harness branch)

When merging branches into `main`:
- **`Models.kt` conflicts**: Use the branch with more `ProviderKind` entries + restore Niumination providers (AGENTROUTER, HUANCHENG, NINE_ROUTER) + add new agent.
- **`PocketDevApp.kt` conflicts**: Restore ALL provider color/mark entries from HEAD, add new agent entries. The deepseek branch removed some providers that Niumination needs.
- **Always verify**: `grep -rn '<<<<<<<' app/` → 0 results

## Pitfalls

- `providersForAgent()` must include the new agent's providers or the provider picker will be empty.
- A new `ProviderKind` breaks every exhaustive `when` over the enum AND every fixed-count assertion on its sets — add branches in the SAME commit (`DshRouteMapper.forProfile`, `updateAgent`, any route mapper) and update size assertions (`assertEquals(N, SET.size)`) plus membership asserts, or CI fails on files you never touched.
- A new bridge must reference only real API surface: real `RuntimeEvent` variants, real `ProviderProfile` fields, real CLI flags verified against the tool's docs, and a constructor signature matching the `MainViewModel` call site (including the `secretFor` lambda). Never invent event names, auth fields, or command flags.
- Guest installers must route through `runGuestCommand`, never bare `process()` + static `check(exit == 0)` — the former streams tool output to the UI and embeds the stderr tail in failures; the latter discards the only evidence of WHY it failed.
- Guest `pip install` commands must be version-aware, not just variant-tolerant: check the package's PyPI `requires_python` against the guest's `python3 --version` FIRST — a `Requires-Python >=X` refusal means the interpreter is too old, and no pip-variant fallback (`python3 -m pip` → `pip3` → `pip`) can fix that. The Python dev-stack overlay supplies pip, never a newer interpreter — pip existing while installs still fail on Requires-Python means the floor is unmet, not the tool missing. Pick the newest interpreter meeting the minimum (`python3.13` → `python3.12` → `python3.11` → `python3`, verified by `sys.version_info`), bootstrap via deadsnakes PPA (`software-properties-common` + `python3.11` + `python3.11-venv` + `ensurepip`) when none qualifies, and invoke the versioned binary directly — never repoint the system `python3` symlink. Keep the PEP 668 tolerance (`--break-system-packages` first, bare fallback) on top of the chosen interpreter.
- An install frozen on a stale progress subtitle with no error is a cancelled coroutine, not a script failure: `runCatching` does not catch `CancellationException`, so any state reset after it is skipped and the UI looks merely stuck — reset install state in `finally`, and distinguish live work from death by `ps -o ARGS` (guest command visible) versus artifacts (binary/marker present), never by re-reading the frozen subtitle.
- Pin one stable CI debug key and gate the artifact: consecutive `assembleDebug` runs mint fresh keys, so on-device updates fail with `INSTALL_FAILED_UPDATE_INCOMPATIBLE` — full recipe (keytool → repo secret → explicit `signingConfig` via env → APK cert-fingerprint assertion) lives in android-adb-testing step 5; never trust implicit `~/.android` placement, it silently no-ops on some runners.
- Never delete "unused" imports/symbols in a cleanup commit without compiling — the compiler is the check, not the eye.
- Gradle task names must be flavor-qualified (`:app:lintOnlineDebug`, not `lintDebug`); every `actions/checkout` needs `submodules: recursive` for the native `third_party/*` sources.
- `AgentRegistry.builtIns()` signature changes — adding a new parameter breaks all call sites.
- `RuntimeBridge` interface methods must all be implemented.
- `isAgentInstalled()` must resolve symlinks INSIDE the rootfs: `File(rootfs, p).canExecute()` follows absolute symlinks (uv tool, pipx entry points) against Android's host root and always reports false — the agent then reinstalls on every tap and post-install verification can never pass. Read the link with `Files.readSymbolicLink`, re-root an absolute target under `rootfs`, and check executability there (the dsh check already carries this workaround; every new agent needs its own instance of it). Apply the SAME helper in `installedAgentVersions()` — it runs its own independent executability check, so fixing only `isAgentInstalled` leaves the runtime-info screen reporting the agent as not installed while installs succeed.
- Prepend the guest user-tools dir (`/root/.local/bin`) to every spawned guest `PATH`: uv/pip CLIs land there, and an interactive terminal spawned with a bare system PATH reports `command not found` for tools the installer just verified present.
- Purge a stale `uv tool` environment before reinstalling into it: `rm -rf ~/.local/share/uv/tools/<pkg>` plus any non-executable shims of its entry points in `~/.local/bin` — reinstalling over a husk left by an interrupted run re-links nothing while reporting success, so the next launch fails on the same dangling symlink the reinstall was supposed to fix.
- **Merge conflict pattern**: `deepseek_harness` may remove providers that Niumination needs. Always compare HEAD vs branch providers before resolving.
- **Hermes is NOT bundled** — requires `pip install` at runtime. Offline support needs a pre-built runtime bundle.
- **Hermes bridge uses stdin/stdout**, not HTTP API — don't confuse with HTTP-based bridges.
- In `app/build.gradle.kts`, Gradle's `Directory.asFile` is already a `File`, not a `Provider` — calling `.get()` on it fails script compilation; for existence checks use plain `rootProject.file(...)`, or make unused bundle tasks pure no-ops that touch no Gradle file API.
- `android-actions/setup-android` accepts ONLY the `packages` input (space-separated string) — `compile-sdk`/`target-sdk`/`min-sdk` inputs do not exist on any version and fail the run at setup time.
- Onboarding Step 2 renders `providersForAgent(agent)` verbatim — a wrong provider SET looks like a UI bug but is a data bug; and `CUSTOM` has no fixed protocol, so EVERY consumer (discovery, validation, `RuntimeLaunchConfigBuilder`, all bridges) must use `profile.effectiveProtocol()`, never `kind.protocol` — always test custom URLs of BOTH families (Anthropic and OpenAI) or Continue 404s on the untested one.
- Gate settings UI on provider kind, not agent kind, when the data model is agent-agnostic — a protocol picker rendered only for one agent silently locks every other agent's custom endpoint to the default protocol, and the resulting 404 looks like a server bug rather than a hidden UI gate.
- Keyless provider kinds must hide the entire key UI (list, add form, save button), not just enable Test without a key — an open key form with zero saved keys reads as a requirement and generates 'it still asks for a key' reports; show a one-line 'no key needed' note naming the actual auth mechanism (device session header) instead.
- Validation success copy must name the endpoint state, never the agent — a hardcoded '<OtherAgent> settings are ready' string on a shared validation path mislabels every agent that reuses it; write 'Connection successful. Settings are ready.' once.
- Failure toasts must not be keyword-gated to auth vocabulary — prefer a denylist (toast every non-blank reason except named-benign ones) over extending an allowlist: under an allowlist each new failure text re-silences itself into timeline rows the user reads as 'no response'. At minimum the filter must also pass install-missing, connectivity, and process-exit reasons ('not installed', 'not found', timeouts, 'exited with code N', 'did not start').
- Triage a red CI run from the failed log file, not the summary line: download `--log-failed` to disk and grep `e: file` for the Kotlin errors — C/C++ `note:` lines from the proot build are noise that outnumber the real error 50:1. A `Suspend function ... can only be called from a coroutine` error means a plain helper gained a suspend call (e.g. a live probe added to diagnostics) — mark the helper `suspend`, do not wrap the call.
- Read the NAME in an `Unresolved reference` error before hunting for a missing symbol: an UPPER_SNAKE name that only ever existed inside an embedded shell string means a lost `$` escape turned the shell variable into a Kotlin template (fix per the shell-dollar bullet below), while a lowercase name that is your own local means a scope error — an accumulator declared inside a `use {}` / `let {}` / `forEach {}` lambda and read after the block is gone from scope; hoist it to function scope and mutate it from inside the lambda. Both cost a full CI cycle each, so classify the name first instead of re-reading the file for a typo.
- Connection validation must echo the server's error body as one truncated line, never a bare HTTP code — a blind `HTTP 400` is undiagnosable while the server's message names the rejected field; and discovery passing (`GET /models`) proves nothing about validation (per-protocol `POST` body), so exercise both before claiming an endpoint works.
- Probe an unknown endpoint key-free before involving real credentials: an invalid-key request returning 401 proves the path exists and auth is layered correctly, while 404 means the path itself is wrong — this separates routing bugs from parameter bugs without touching secrets.
- Agents that sign in via OAuth rather than API keys must skip the provider step with an explanatory empty-state — rendering an empty provider list dead-ends the wizard.
- When syncing docs, grep every cited class/event/field against the code first — integration docs rot into fictional API references within days of refactors.
- **CI builds and releases the online APK** — `.github/workflows/build.yml` runs lint + unit tests + `:app:assembleOnlineDebug` and uploads `app-online-debug.apk` to GitHub Releases on every `main` push. CI debug builds each carry a fresh ephemeral signature, so on-device test loops cannot `install -r` across builds — uninstall between builds or commit a persistent debug keystore to CI. The release step re-uses a fixed tag, so each run REPLACES the asset instead of creating a new release — `gh release view` keeps showing the old `publishedAt`; confirm the new build landed via the asset's `updatedAt`: `gh release view <tag> --json assets --jq '.assets[] | "\(.name) updated=\(.updatedAt)"'`.
- **Debug APKs are blocked by Play Protect** — always use `-PplayBuild=true assembleRelease` for installable APKs, or use ADB sideload for testing.
- Before deleting a file as dead code, prove every top-level symbol is private AND unreferenced — grep call sites for each name, and beware substring matches (a grep for `InfoRow(` also hits `RuntimeInfoRow(`). All-private with zero external callers is safe for `git rm`; anything less is a compile-and-verify deletion, not an obvious one.
- Write shell dollars inside Kotlin strings as `${'$'}`, never `\$` — a backslash before `$` can vanish in transit and land as a bare `$`, which Kotlin parses as a string template and fails with `Unresolved reference` for every shell variable. Type exactly ONE backslash per remaining Kotlin escape (`\"`, `\n`) — the patch tool writes bytes literally and never doubles, so hand-typed doubles land in source and break guest scripts at runtime while compilation stays green. Never copy escape sequences out of displayed diffs or tool output: the transport doubles every backslash on display, so pasted doubles corrupt the file. After any hand-edit of nested escapes (shell inside Kotlin strings), verify bytes BEFORE compiling with BOTH checks — a doubled-backslash scan alone passes while every `\$` is already missing: (1) `repr()` the hunk lines via `python3 -c` to confirm single backslashes, and (2) grep the hunk for bare `$` followed by a shell identifier to confirm no template accident survives; `od -c` is the fallback when a green build already misbehaves on-device, since escape corruption is invisible in diffs.
- Documentation is NOT optional — create integration doc + development guide + AGENTS.md in the same commit as the code changes, and never land code first with docs in a follow-up commit: the owner reads a split as an incomplete change and asks why it was not one commit. Audit notes and fix plans written alongside the code belong in that same commit.
- Every installable agent needs an entry in the update-check path (`checkAgentUpdates()` or equivalent) — without one, the UI can never offer reinstall/update and the install button stays disabled once installed, which users report as 'cannot reinstall'. Wire install + update-check + update in the same commit when adding an agent; when a user reports reinstall blocked, audit update-check coverage before touching install logic.
- Verify the guest package source carries the feature you depend on: compare the registry release date (PyPI `upload_time`) against the feature's birth commit date. A tool that works on a dev checkout but reports 'not configured' / 'unknown provider' in the guest is usually version skew, not a config bug. When the latest registry release predates the feature, install from a pinned git checkout plus `uv sync --locked` venv — shallow clone, checkout the verified SHA, then `UV_PROJECT_ENVIRONMENT=$SRC/venv uv sync --locked` (core first, `--extra all` on retry), mirroring the tool's official installer layout. Registry-style installs (`pip`/`uv tool install`, even from a source tarball) are unsupported upstream and can fail to build or time out on-device — demote tarball and registry to fallback layers, never the primary. Record the pinned build in the install marker so the update path can detect drift. The upstream installation path is the shell installer (`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`), which clones the repo and builds a `uv sync` venv — registry installs (`pip`, `uv tool install`, even from a source tarball) are declared UNSUPPORTED upstream, so they stay fallback layers only. That installer also stages down for constrained guests (`--skip-browser --skip-computer-use --skip-setup` drops the Node/Chromium downloads), so on a phone guest replicate just the repo+venv stages instead of dragging hundreds of MB of browser tooling in.
- A green connectivity probe that bypasses the real execution path certifies nothing: an HTTP Test button and a presence-based Doctor both pass while chat — which runs a guest CLI of a different version with its own provider wiring — fails every time. Either route the probe through the real path (dry-run the exact guest command, assert the guest binary version resolves the provider) or label the UI honestly as reachability-only. Presence (binary exists, marker present, HTTP 200) is not capability; a green dashboard over an incapable binary actively misleads triage.
- Opening a spawn output file immediately after launch races native file creation: a slow proot fork means the first reader gets ENOENT while the file appears a moment later, and the session is already marked failed. Wait bounded-ly for the file to exist (or open the stream lazily) before declaring the launch dead.
- A live tail reader also races the guest's writes at the OTHER end: the file exists but is still empty when opened, `readLine()` hits EOF instantly, and the answer landing later is never streamed — the session 'completes' with nothing shown while the output file holds the full answer. After process exit, reconcile: re-read the finished file, drop the already-emitted prefix, and emit the rest as deltas under the same banner/blank filter.
- When the guest output file holds an answer the UI never shows, suspect the ViewModel event gates before rewriting the bridge: `onRuntimeEvent` drops everything while `isRunning` is false or when `activeSessionId` mismatches (e.g. a stale id from a session that never completed), so a working bridge still reads as 'no response' — confirm gate state from the persisted session file (mtime plus content) and the output file first.
- Never offer a provider or option the bridge cannot execute: a route mapper returning null for an offered choice turns that UI option into a guaranteed failure with a confusing message. Either implement the mapping — writing the guest config from the app so it becomes the single source of truth for base URL, model, and key — or remove the option for that agent.
- A one-shot CLI wrapped as 'chat' has no memory unless history is threaded in: accepting a `conversationHistory` parameter but never passing it makes every message stateless while the UI promises continuity. Either inject prior turns (or a rolling summary) into each invocation or label the mode honestly; verify with a two-message recall probe before claiming chat works.
- Never persist speculative UI state into the permanent transcript on every event: interrupted/live blocks written per streamed line accumulate duplicates that crash keyed lists (duplicate key = FATAL). Persist only settled messages per event; if transient blocks must be stored, give each a unique id and dedupe on load.

## Documentation Requirements

Every agent integration commit MUST include:
1. `docs/<AGENT>-INTEGRATION.md` — architecture, installation, communication protocol, debugging
2. `docs/DEVELOPMENT-GUIDE.md` — project overview, adding agents pattern, testing, build variants
3. `AGENTS.md` in project root — file mapping, workflow, dependencies
4. README.md updates — coding agents table, runtime components, limitations

See [DEVELOPMENT-GUIDE.md](docs/DEVELOPMENT-GUIDE.md) for the complete guide.

## CI/CD and Build APK

### GitHub Actions CI
The CI workflow (`.github/workflows/build.yml`) has three jobs — lint, unit
tests, and **Build & Release APK** — and publishes the APK to GitHub
Releases automatically on every `main` push:
- `:app:lintOnlineDebug :app:lintOfflineDebug` — static analysis, both flavors
- `:app:testOnlineDebugUnitTest :app:testOfflineDebugUnitTest` — unit tests
- `:app:assembleOnlineDebug` with `-PplayBuild=true` (targetSdk 36, Play
  Protect-compatible sideload) → `softprops/action-gh-release` uploads
  `app/build/outputs/apk/online/debug/app-online-debug.apk`
- All checkouts use `submodules: recursive` (CMake needs
  `third_party/proot` and `third_party/libandroid-shmem`)
- The `online` flavor is the shippable CI artifact (runtime downloaded
  on demand); `offline` needs prebuilt bundles absent from CI.

### Building APK Locally

**Debug APK (NOT Play Protect safe):**
```bash
./gradlew assembleDebug
```
- Uses `targetSdk 28`, unsigned debug key, has test API keys
- **Play Protect WILL block installation**

**Play Protect-safe Release APK (requires upload keystore):**
```bash
./gradlew -PplayBuild=true assembleRelease
```
- Uses `targetSdk 36`, signed with upload keystore
- Requires environment variables: `MH_UPLOAD_STORE_FILE`, `MH_UPLOAD_STORE_PASSWORD`, `MH_UPLOAD_KEY_ALIAS`, `MH_UPLOAD_KEY_PASSWORD`
- Keystore: `/Users/jarves/.mobile-harness/mobile-harness-upload.jks`

**Play-optimized Debug (targetSdk 36, still unsigned):**
```bash
./gradlew -PplayBuild=true :app:assembleOnlineDebug
```
- Sideloadable via file manager with no ADB, cable, or Android Studio — copy `app/build/outputs/apk/online/debug/app-online-debug.apk` to the phone and install (targetSdk 36 satisfies Play Protect on Android 13+)

### How to Make an APK Safe for Play Protect
1. **Always use `-PplayBuild=true`** — sets `targetSdk 36` and `IS_PLAY_BUILD=true`
2. **Sign release builds with the upload keystore** — unsigned `-PplayBuild=true` debug APKs still install fine; signing is required for Play Store distribution, not for sideload testing
3. **Install `-PplayBuild=true` debug APKs directly via file manager** — it is plain `assembleDebug` (targetSdk 28) that Play Protect blocks on Android 13+
4. **For sideload testing**: copy the online-flavor APK to the phone and install via file manager — no ADB needed

### Play Protect Block Reasons
| Cause | Fix |
|-------|-----|
| Unsigned APK | Sign with upload keystore |
| targetSdk < 36 | Use `-PplayBuild=true` |
| Test API keys in BuildConfig | Release build strips test keys |
| Debug signing key | Use release signing config |

### Build Script
`scripts/build-play-release.sh` automates the release build with Play Store readiness checks. It reads the keystore from macOS Keychain (`com.jarves.mh` service).

## On-Device Testing via ADB

Physical-device loop for verifying CI-built APKs while the owner holds the phone on cable. The owner taps; you observe via screenshot + logcat and push fixes through CI.

1. `adb devices -l` must list the device; `adb shell getprop` accepts exactly ONE property per invocation.
2. Download the exact Release asset (`gh release download <tag> -p 'app-online-debug.apk'`) — never test a stale local build; compare byte sizes across runs to confirm the new build actually landed.
3. Uninstall before install (`adb uninstall <pkg>` then `adb install`) whenever the signing key may differ — CI debug builds rotate signatures, so `install -r` fails with `INSTALL_FAILED_UPDATE_INCOMPATIBLE`.
4. Launch explicitly (`adb shell am start -n <pkg>/.MainActivity`); confirm with `pidof` plus the focused-activity dumpsys, not with the installer exit code.
5. Capture with `adb exec-out screencap -p > stepN.png` and inspect each screen before instructing the next tap; pull filtered logcat (`adb logcat -d | grep -i <keywords>`) in the same pass for server messages the UI truncates.
6. While an install runs, `adb shell ps -A -o ARGS` shows the exact guest command live on the phone — it proves which build's code path is executing and carries text the UI subtitle truncates. No matching process plus no new binary means the phase already ended: re-check artifacts instead of assuming progress.
6. Credentials stay on the device — the owner types keys into the phone UI; never ask for a key and never probe authenticated endpoints from your own machine with anything but an intentionally invalid key.

## Verification
- `grep -rn '<<<<<<<' app/` → 0 results
- `grep -n 'AgentKind.NEW_AGENT' app/src/main/java/com/jarves/mh/` → appears in Models, AgentDriver, RuntimeInstaller, MainViewModel, PocketDevApp
- `grep -n 'hermesRuntime\|HermesRuntimeBridge' app/src/main/java/com/jarves/mh/ui/MainViewModel.kt` → present
- `grep -n '<name>Runtime.events.collect' app/src/main/java/com/jarves/mh/ui/MainViewModel.kt` → 1 result (bridge referenced without this line is dead UI — see Step 6)
- `grep -n 'playBuild=true\|-PplayBuild' scripts/README` → build instructions documented
- Build succeeds
- Documentation committed: `docs/HERMES-AGENT-INTEGRATION.md`, `docs/DEVELOPMENT-GUIDE.md`, `AGENTS.md`

## References

- [Build APK Guide](references/build-apk-guide.md) — detailed build commands, Play Protect requirements, signing workflow
- [OpenCode Endpoint Quirks](references/opencode-endpoint-quirks.md) — Zen free-tier lock, Go `x-opencode-session` header, discovery-vs-validation asymmetry
