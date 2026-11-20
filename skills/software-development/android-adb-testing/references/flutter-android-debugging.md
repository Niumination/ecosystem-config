# Flutter on Android — Debugging & Build Pitfalls

When testing Flutter apps on physical Android devices via ADB, several platform-specific gotchas appear repeatedly. This covers the ones most often missed on first encounter.

---

## Build Environment Requirements

Flutter on Android requires these to be present and correctly versioned:

| Component | Minimum Version | Notes |
|-----------|----------------|-------|
| Flutter SDK | ≥3.16 | Check with `flutter --version` |
| Java | 17 or 21 | Set `JAVA_HOME`; older projects need specific minor version |
| Android SDK Platform Tools | Current | `platform-tools` must include `adb` |
| Android NDK | r25+ recommended | Required for native plugins; must have `toolchains/llvm/prebuilt/` |

If `flutter doctor` reports NDK issues, the most common fix is a full re-extract from Google:
```bash
wget https://dl.google.com/android/repository/android-ndk-r26b-darwin.zip
unzip android-ndk-r26b-darwin.zip -d /usr/local/Caskroom/android-platform-tools/<sdk_version>/
ln -sf android-ndk-r26b ndk/27.0.12077973
```

Symlink stubs (empty `clang` files) cause silent compile failures — verify with `ls -la ndk/*/toolchains/llvm/prebuilt/darwin-x86_64/bin/clang`.

---

## Debug APK Blocked by Device Security

Some manufacturers (Transsion group: Infinix, Tecno, Itel; Xiaomi; Huawei) block debug APK installation via `INSTALL_FAILED_VERIFICATION_FAILURE`. This is a system-level policy, NOT a build error.

**Diagnosis:** `adb install` returns `Failure [INSTALL_FAILED_VERIFICATION_FAILURE]` while release APK installs fine.

**Workarounds (in order of preference):**
1. Use release build: `flutter build apk --release` then `adb install app-release.apk`
2. Disable Google Play Protect temporarily: Settings → Google → Play Protect → turn off
3. Install via `flutter run` which uses a different push path that sometimes bypasses the gate

Release APKs are signed with a debug key by default in Flutter — they won't pass Play Store verification but will install without the security gate.

---

## Logging Strategy

### Logcat Filtering
```bash
# Clear buffer, then capture after user action
adb logcat -c
adb shell am start -n <package>/.MainActivity

# After action, filter for flutter tag
adb logcat -d | grep 'flutter'

# Or PID-filtered for cleaner output
adb logcat -d --pid=$(adb shell pidof <package>)
```

### Custom Debug Prints
Insert `print('DEBUG: ...')` anywhere in Dart code. These surface in logcat as:
```
I/flutter: DEBUG: Collecting device info...
```

**Pro tip:** Add structured prefixes to make grepping easier:
- `print('DEBUG[login]: calling api with nip=$nip')`
- `print('ERROR[auth]: ${e.toString()}')`

### Common Log Noise to Exclude
Vendor frameworks produce tons of irrelevant output. Pipe through:
```bash
adb logcat -d | grep 'flutter' | grep -vE 'transsion|Thermal|TPMS|ScnModule|START_DEBUG'
```

---

## Dio HTTP Client Gotchas

### Non-2xx Responses Throw Exceptions

Dio's default `validateStatus` only accepts 2xx. A 422 Unprocessable Entity from your API will throw `DioException(type: DioExceptionType.badResponse)` BEFORE you can read the response body.

**Fix:** In your Dio client configuration:
```dart
_dio = Dio(BaseOptions(
  baseUrl: ApiEndpoints.base,
  validateStatus: (status) => status != null && status < 500,
));
```

This lets 4xx responses through so you can parse the server's error JSON.

### Catch Order Matters

Always catch `DioException` BEFORE generic `Exception`:
```dart
try {
  final resp = await api.login(nip: nip, password: password);
} on DioException catch (e) {
  // e.type: connectionTimeout, sendTimeout, badResponse, etc.
  // e.response?.data has the JSON error body
  print('DioError type=${e.type}, message=${e.message}');
} on Exception catch (e) {
  // Other exceptions (network down, etc.)
}
```

### CSRF Cookie Flow (Laravel Sanctum)

Many Laravel APIs use Sanctum for CSRF protection. The flow is:
1. GET `/sanctum/csrf-cookie` — sets `XSRF-TOKEN` cookie
2. POST to login endpoint with that cookie included

Dio handles this automatically if both requests share the same `Dio` instance (cookie jar persists across calls). Verify by checking `cookies` in the Dio instance after the CSRF fetch.

---

## Impeller vs Skia Renderer

Flutter 3.29+ defaults to Impeller (Vulkan renderer). Some Mali-G GPU devices (common in budget/mid-range phones like Infinix) don't support all Impeller features, causing black/blank screens on launch.

**Symptoms:** App launches, no crash, but screen stays black or shows nothing.

**Diagnosis:** Check logcat for:
```
I/flutter: Using the Impeller rendering backend (Vulkan)
```
Then look for Vulkan validation errors below it.

**Fix options:**
1. Force Skia (default before 3.29): Not easily doable post-build; requires embedding flag
2. Wait for device driver update
3. Test on a different device with Adreno GPU (Qualcomm) — Impeller works reliably there

Most production apps still ship successfully because the fallback to Skia kicks in for unsupported features. Black screen usually means a complete render failure requiring a Flutter framework update or device-specific workaround.

---

## Quick Reference: Error Patterns

| Symptom | Likely Cause | First Check |
|---------|-------------|-------------|
| `INSTALL_FAILED_VERIFICATION_FAILURE` | Manufacturer security gate | Switch to release APK |
| Black screen on launch | Impeller incompatibility | Check logcat for Vulkan errors |
| `DioException: badResponse` on 422 | Missing `validateStatus` config | Add `status < 500` to BaseOptions |
| NDK error at build time | Partial/corrupt NDK extract | Re-extract full NDK zip |
| `pidof` returns empty | App crashed on startup | `adb logcat -d --pid=<old_pid>` before new launch |
