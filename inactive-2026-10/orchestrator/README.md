# orchestrator

Multi-agent workflow coordinator — dispatch tasks to agents, monitor progress,
and orchestrate complex multi-step pipelines from a single local hub.

> **Phase:** Scaffold (Phase 1 of 6)
> **Stack:** Python 3.11+ · Pydantic v2 · Typer · Rich

---

## Quick Start

```bash
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode
pip install -e ".[dev]"

# See CLI help
python -m orchestrator --help
```

## Usage

```bash
# Show system info
python -m orchestrator info

# Validate the environment is ready
python -m orchestrator check
```

## Configuration

By default the orchestrator uses sensible built-in defaults.
Create an `orchestrator.yaml` or set `ORCHESTRATOR_*` environment variables
to override:

```yaml
sqlite_path: ~/.orchestrator/orchestrator.db
agent_timeout_seconds: 300
log_level: INFO
max_concurrent_agents: 4
```

## Project Roadmap

| Phase | What                                       |
|-------|--------------------------------------------|
| 1     | Project scaffold (✅ this)                  |
| 2     | Data models & SQLite persistence           |
| 3     | Kanban board integration                   |
| 4     | Orchestrator engine + agent adapters       |
| 5     | Web dashboard (Niu-Kanban Dash v3)        |
| 6     | Observability & alerting                   |

---

Built by [Niumination](https://github.com/Niumination)
