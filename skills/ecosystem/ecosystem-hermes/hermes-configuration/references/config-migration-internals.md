# Config Migration Internals

## `_config_version` System

`hermes_cli/config_defaults.py` defines `_config_version: 41` (as of v0.21.1). This is the current schema version.

Every time a new schema field is added that requires migration, `_config_version` is bumped and a migration step is added to `MIGRATIONS` in `hermes_cli/config_migrations.py`.

### How it works

1. `check_config_version()` compares on-disk `_config_version` to `DEFAULT_CONFIG._config_version`
2. If current < latest, `_check_and_apply_config_migration()` runs during `hermes update`
3. `run_migrations(current_ver, results, quiet)` iterates `MIGRATIONS` registry
4. Each `(target_ver, migration_fn)` pair is applied when `current_ver < target_ver`
5. After migrations, `migrate_config()` handles missing env vars and new config fields interactively

### `MIGRATIONS` Registry

Located in `hermes_cli/config_migrations.py`. Strictly ascending tuple of `(target_version, migration_fn)`:

```python
MIGRATIONS = (
    (12, _migrate_to_12),
    (13, _migrate_to_13),
    ...
    (39, _migrate_to_39),
    (40, _rewrite_stale_default(...)),  # model_catalog.ttl_hours → ttl_minutes
    (41, _migrate_to_41),               # SOUL.md Bot Mode cleanup
)
```

Version gaps (15, 18-20, 22, 24, 26-28, 30) only added a schema default that runtime merging supplies without a write.

### `_config_version` floor gate

`SUPPORT_FLOOR_VERSION = 12`. Configs with on-disk version below 12 are NOT migrated and NOT rewritten — a message is shown instead.

### What migrations do NOT do

- Do NOT auto-populate runtime-configured fields like `home_channel` (PlatformConfig field not in DEFAULT_CONFIG)
- Do NOT reset user-configured values — deep-merge only adds new defaults, never overwrites existing
- Do NOT touch platform adapter settings like `SUPPORTS_NATIVE_STREAMING`

### Fields that require separate setup

These are NOT in `DEFAULT_CONFIG` and must be configured separately:
- `platforms.<platform>.home_channel` — runtime field, set via `/set home`
- `platforms.<platform>.enabled` — defaults to `False`, user must enable
- `platforms.<platform>.token` — secrets managed separately

## Update Safety

`hermes update` pipeline:
1. Plan → Snapshot (pre-update backup per profile)
2. Apply → git pull or zip fallback (refuses dirty working tree)
3. Restart-per-kind → systemd/Launchd restart
4. Verify → `gateway_state.json` code_version stamps
5. Report → machine-readable receipt in `~/.hermes/logs/update_receipts/`
6. **Config migration** → `_check_and_apply_config_migration()` with freshly-reloaded modules
7. **Skills sync** → bundled skills synced to `~/.hermes/skills/`

### Key safeguard

If an update is interrupted after code pull but before config migration, the next `hermes` invocation detects and applies the migration. See #91360.

## Config Restoration from Backup

When config drifts:
1. `diff ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.<timestamp>`
2. Restore using `hermes config set <path> <value>`
3. NEVER edit config.yaml directly — security filter refuses `write_file`/`patch` on config.yaml
4. Verify with `hermes config show` and `hermes status`

## PlatformConfig Dataclass

Located in `gateway/config.py`:

```python
class PlatformConfig:
    enabled: bool = False
    token: Optional[str] = None
    gateway_restart_notification: bool = True
    home_channel: Optional[HomeChannel] = None
    reply_to_mode: str = "first"
    typing_indicator: bool = True
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlatformConfig":
        # top-level keys win over extra; missing keys get defaults
```

Fields like `home_channel` are read from the YAML at runtime via `get_home_channel(platform)`. If not set, returns `None`.
