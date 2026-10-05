"""Configuration loading — YAML / environment variable overrides.

Priority (highest wins):
  1. Environment variable ``ORCHESTRATOR_<KEY>``
  2. YAML config file (``--config`` / ``ORCHESTRATOR_CONFIG`` / ``./orchestrator.yaml``)
  3. Sensible defaults defined in :class:`OrchestratorConfig`
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings

from orchestrator.types import DEFAULT_AGENT_TIMEOUT_SECONDS, DEFAULT_LOG_LEVEL, DEFAULT_SQLITE_PATH, LogLevel


class OrchestratorConfig(BaseSettings):
    """Top-level orchestrator configuration model.

    Every field is auto-populated from the environment via the prefix
    ``ORCHESTRATOR_`` (e.g. ``ORCHESTRATOR_LOG_LEVEL=DEBUG``)  The
    :meth:`from_yaml` factory merges a YAML file on top of defaults but
    *below* env overrides.
    """

    model_config = {
        "env_prefix": "ORCHESTRATOR_",
        "env_nested_delimiter": "__",
        "extra": "ignore",
    }

    # ── Paths ──────────────────────────────────────────────────────────────

    sqlite_path: Path = Field(
        default=Path(DEFAULT_SQLITE_PATH).expanduser().resolve(),
        description="Filesystem path for the orchestrator SQLite database.",
    )

    config_path: Path | None = Field(
        default=None,
        description="Path to the YAML config file that was loaded (if any).",
    )

    # ── Behaviour ──────────────────────────────────────────────────────────

    agent_timeout_seconds: int = Field(
        default=DEFAULT_AGENT_TIMEOUT_SECONDS,
        ge=10,
        le=86_400,
        description="Max wall-clock seconds an agent run may take before being timed out.",
    )

    log_level: LogLevel = Field(
        default=DEFAULT_LOG_LEVEL,
        description="Root logger verbosity.",
    )

    log_format: Literal["plain", "json"] = Field(
        default="plain",
        description="Output format for log records.",
    )

    # ── Agent pool ─────────────────────────────────────────────────────────

    max_concurrent_agents: int = Field(
        default=4,
        ge=1,
        le=64,
        description="Maximum number of agents the orchestrator may dispatch in parallel.",
    )

    # ── Lifecycle ──────────────────────────────────────────────────────────

    db_poll_interval_seconds: float = Field(
        default=2.0,
        ge=0.1,
        le=60.0,
        description="How often the scheduler polls the DB for new tasks.",
    )

    stale_run_timeout_seconds: int = Field(
        default=300,
        ge=30,
        le=86_400,
        description="Seconds with no heartbeat before a run is considered stale / dead.",
    )

    # ── Convenience ────────────────────────────────────────────────────────

    @field_validator("sqlite_path", mode="before")
    @classmethod
    def _resolve_path(cls, v: str | Path) -> Path:
        return Path(v).expanduser().resolve()

    @classmethod
    def from_yaml(
        cls,
        path: str | Path | None = None,
        *,
        _env_overrides: bool = True,
    ) -> OrchestratorConfig:
        """Build config from a YAML file, then overlay env vars.

        If *path* is ``None`` the loader tries, in order:
        ``$ORCHESTRATOR_CONFIG`` → ``./orchestrator.yaml`` → defaults only.
        """
        # 1. Start from env-driven defaults (BaseSettings does this)
        base = cls() if _env_overrides else cls(_env_file=None)

        # 2. Resolve YAML path
        if path is None:
            path = os.environ.get("ORCHESTRATOR_CONFIG") or "./orchestrator.yaml"

        yaml_path = Path(path).expanduser().resolve()
        if not yaml_path.exists():
            # No YAML file — pure env/defaults
            base.config_path = None
            return base

        # 3. Load YAML dict
        with yaml_path.open("r") as fh:
            raw: dict = yaml.safe_load(fh) or {}

        # 4. Merge YAML → BaseSettings (env still wins because BaseSettings
        #    constructor re-applies env_prefix on top)
        merged = cls(**{**raw, "config_path": str(yaml_path)})
        return merged


def load_config(path: str | Path | None = None) -> OrchestratorConfig:
    """Shortcut — load and return the resolved config.

    Raises ``SystemExit`` on validation errors so CLI consumers get a clear
    error message without a raw traceback.
    """
    try:
        return OrchestratorConfig.from_yaml(path)
    except ValidationError as exc:
        from rich.console import Console

        console = Console(stderr=True)
        console.print("[red]Config validation error:[/red]")
        for err in exc.errors():
            loc = " → ".join(str(l) for l in err["loc"]) if err["loc"] else "(root)"
            console.print(f"  • {loc}: {err['msg']}")
        raise SystemExit(1) from exc
