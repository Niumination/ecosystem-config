# Emulator UI-tree QA (Flutter)

Adapted from `openai/plugins` — `plugins/test-android-apps/skills/android-emulator-qa` (commit `981b02c`, Apache-2.0; see `../scripts/ATTRIBUTION.md`). The upstream Gradle commands are replaced with Flutter commands; helper scripts are vendored unmodified.

## Build and launch

- Build the Flutter artifact instead of calling Gradle directly: `flutter build apk --debug`, then `adb install -r build/app/outputs/flutter-apk/app-debug.apk`. Keep the signature-identity checks in `../SKILL.md` unchanged.
- Resolve the launcher activity before starting: `adb shell cmd package resolve-activity --brief <id>` — do not hard-code `/.MainActivity` when the Flutter project renamed it.

## Coordinates from the UI tree

Drive taps from the UI tree, never from screenshot pixel guessing:

1. `adb exec-out uiautomator dump /dev/tty > /tmp/ui.xml`
2. `python3 <skill>/scripts/ui_pick.py /tmp/ui.xml "<exact label>"` prints the centre `x y`; tap with `adb shell input tap x y`.
3. `python3 <skill>/scripts/ui_tree_summarize.py /tmp/ui.xml /tmp/ui-summary.txt` gives a compact view before choosing a target.
4. If the node is absent but a `scrollable` parent exists, swipe and re-dump at least once before declaring it missing. Keep swipes ~150-200 px away from screen edges to avoid back gestures.

The helpers are Python stdlib only (no network/exec). Regression coverage: `python3 -m unittest discover -s <skill>/tests`.

## Verification

Each action gets a fresh device screenshot and a pid-filtered logcat window from the main procedure — the UI tree supplies coordinates, the screenshot supplies visual confirmation.
