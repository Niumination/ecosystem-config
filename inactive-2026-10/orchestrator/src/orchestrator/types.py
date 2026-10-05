"""Type aliases, constants, and enums used across the orchestrator."""

from __future__ import annotations

from enum import Enum
from typing import TypeAlias
from uuid import UUID

# ── Identifiers ──────────────────────────────────────────────────────────────

AgentID: TypeAlias = str
"""Unique identifier for an agent (e.g. ``"opencode"`` or ``"codex"``)."""

TaskID: TypeAlias = str
"""Unique identifier for a task (e.g. ``"t_abc123"``)."""

RunID: TypeAlias = UUID
"""Unique identifier for a single run of a task."""

# ── Enums ────────────────────────────────────────────────────────────────────


class AgentStatus(str, Enum):
    """Current liveness state of an agent."""

    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"


class TaskStatus(str, Enum):
    """Lifecycle states a task can be in."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class LogLevel(str, Enum):
    """Log verbosity levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ── Constants ────────────────────────────────────────────────────────────────

DEFAULT_SQLITE_PATH = "~/.orchestrator/orchestrator.db"
"""Default path for the orchestrator's SQLite state database."""

DEFAULT_AGENT_TIMEOUT_SECONDS = 300
"""Max seconds an agent may run before being considered stalled."""

DEFAULT_LOG_LEVEL = LogLevel.INFO
"""Default verbosity for orchestrator logging."""

ORCHESTRATOR_VERSION = "0.1.0"
"""Current software version, kept in sync with pyproject.toml."""
