# Mobile-Harness Build APK Guide

## Quick Reference

### Build Commands

| Command | Play Protect Safe? | Requires Keystore? |
|---------|:---:|:---:|
| `./gradlew assembleDebug` | ❌ No | No |
| `./gradlew -PplayBuild=true assembleDebug` | ⚠️ Maybe | No |
| `./gradlew -PplayBuild=true assembleRelease` | ✅ Yes | **Yes** |
| `./gradlew -PplayBuild=true bundleRelease` | ✅ Yes | **Yes** |
| `scripts/build-play-release.sh` | ✅ Yes | **Yes** (Keychain) |

### CI vs Local Build

**GitHub Actions CI** (`.github/workflows/build.yml`):
- Only runs `lintOnlineDebug` and `testOnlineDebugUnitTest`
- **Does NOT build APK**
- To add APK building: create a new job with signing credentials as GitHub Secrets

**Local build**: Use `./gradlew` commands directly

### Making an APK Safe for Play Protect

1. **Always use `-PplayBuild=true`** — sets `targetSdk 36` and `IS_PLAY_BUILD=true`
2. **Always sign with the upload keystore** — unsigned APKs are blocked
3. **Required env vars**:
   - `MH_UPLOAD_STORE_FILE` — path to `.jks` keystore
   - `MH_UPLOAD_STORE_PASSWORD` — keystore password
   - `MH_UPLOAD_KEY_ALIAS` — key alias
   - `MH_UPLOAD_KEY_PASSWORD` — key password
4. **Keystore location**: `/Users/jarves/.mobile-harness/mobile-harness-upload.jks`
5. **Keychain service**: `Mobile Harness Upload Key` (macOS Keychain account `com.jarves.mh`)

### ADB Sideload (Testing Without Play Protect)

```bash
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

ADB sideload bypasses Play Protect entirely — useful for development testing.

### Play Protect Block Reasons

| Cause | Fix |
|-------|-----|
| Unsigned APK | Sign with upload keystore |
| targetSdk < 36 | Use `-PplayBuild=true` |
| Test API keys in BuildConfig | Release build strips test keys |
| Debug signing key | Use release signing config |

### Build Script Details

`scripts/build-play-release.sh` automates:
- Keystore lookup from macOS Keychain
- `playReadinessCheck` validation
- Unit tests + lint
- `assembleRelease` + `bundleRelease`
- Output: `.aab` (Play Store) + `.apk`

Usage:
```bash
./scripts/build-play-release.sh <version_code> <version_name>
```

### Important Notes

- `targetSdk = if (playBuild) 36 else 28` — debug defaults to 28
- `applicationId = "com.jarves.mh"` — fixed
- `versionCode = 4` / `versionName = "1.0.3"` — defaults
- ARM64-only native output (`ndk.abiFilters += "arm64-v8a"`)
- `offline` product flavor available for bundled runtime
- `online` product flavor (default) downloads runtime from CDN

## References

- `app/build.gradle.kts` — full build configuration
- `scripts/build-play-release.sh` — automated release build script
- `.github/workflows/build.yml` — CI workflow (lint + test only)