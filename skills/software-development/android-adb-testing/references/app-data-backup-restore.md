# App-Data Backup & Restore (run-as tar pipes)

For signature-forced reinstalls (`INSTALL_FAILED_UPDATE_INCOMPATIBLE`):
uninstall wipes `/data/user/0/<pkg>` including downloaded runtimes, so
stream app-private data to the Mac first. `run-as` stdout/stdin pipes
work even where `adb pull` cannot reach.

## Backup

```bash
adb shell run-as <pkg> tar -czf - /data/user/0/<pkg>/files/workspaces \
  /data/user/0/<pkg>/files/chats /data/user/0/<pkg>/files/checkpoints \
  /data/user/0/<pkg>/files/terminal-history /data/user/0/<pkg>/files/setup \
  /data/user/0/<pkg>/files/runtime/ubuntu/workspace/<project> > backup.tgz
```

Members MUST be absolute — `run-as` cwd is unreliable, never `cd`.
Skip the bulk runtime rootfs (re-downloadable, often ~1GB); take only the
irreplaceable project dir inside it.

## Verify (mandatory — pipes fail silently)

```bash
tar -tzf backup.tgz | grep -E "<project>|<auth-dir>|profileInstalled|setup/" | head
```

A 0-byte file or missing keys means the pipe broke — do NOT uninstall yet.

## Restore (rooted, so the package dir itself is never a member)

Re-tar the subset on the Mac rooted at `files/`, then pipe back with `-C`
pointing INSIDE the package dir:

```bash
tar -xzf backup.tgz -C /tmp/restore <wanted members>
cd /tmp/restore/data/user/0/<pkg> && tar -czf - files \
  | adb shell run-as <pkg> tar -xzf - -C /data/user/0/<pkg>
```

**Mode-clobber hazard (why the rooting matters):** re-tarring on the Mac
bakes Mac dir modes (755) into the archive; if the package data dir itself
is an archive member, extraction chmods it and `run-as` then refuses every
call (`readable or writable by others`). Rooting the archive below the
package dir avoids this entirely. `pm clear` does NOT repair a clobbered
top-dir mode (it wipes contents only) — only a reinstall recreates it.

## After reinstall

- The hardware Keystore is wiped with the app: provider API keys must be
  re-typed on the device by the owner. Never ask for them in chat.
- Guest-rootfs projects restore only AFTER first-run re-downloads the
  runtime (the target path does not exist before that).
