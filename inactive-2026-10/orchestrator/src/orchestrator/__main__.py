"""CLI entry point — run via ``python -m orchestrator``."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from orchestrator import __version__
from orchestrator.config import load_config
from orchestrator.types import ORCHESTRATOR_VERSION

app = typer.Typer(
    name="orchestrator",
    help="Multi-agent orchestrator — dispatch, monitor, and coordinate agent workflows.",
    no_args_is_help=True,
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to YAML configuration file.",
        exists=False,
        file_okay=True,
        dir_okay=False,
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version and exit.",
    ),
) -> None:
    """Orchestrator — coordinate multi-agent workflows from your local hub."""
    if version:
        console.print(f"orchestrator v{__version__}")
        raise typer.Exit()

    # Load config and stash on context so sub-commands can access it
    cfg = load_config(config)
    ctx.ensure_object(dict)
    ctx.obj["config"] = cfg


@app.command()
def info(ctx: typer.Context) -> None:
    """Display current configuration and system information."""
    cfg = ctx.obj["config"]

    table = Table(title="orchestrator  —  System Info")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Version", ORCHESTRATOR_VERSION)
    table.add_row("Config file", str(cfg.config_path or "(defaults)"))
    table.add_row("SQLite path", str(cfg.sqlite_path))
    table.add_row("Log level", cfg.log_level.value)
    table.add_row("Agent timeout", f"{cfg.agent_timeout_seconds}s")
    table.add_row("Max concurrent", str(cfg.max_concurrent_agents))
    table.add_row("DB poll interval", f"{cfg.db_poll_interval_seconds}s")
    table.add_row("Stale run timeout", f"{cfg.stale_run_timeout_seconds}s")

    console.print(table)


@app.command()
def check(ctx: typer.Context) -> None:
    """Validate that the orchestrator is ready to run (DB, paths, config)."""
    cfg = ctx.obj["config"]

    ok = True

    # ── SQLite path ──────────────────────────────────────────────────────
    db_dir = cfg.sqlite_path.parent
    if db_dir.exists():
        console.print(f"[green]✔[/green] DB directory exists: {db_dir}")
    else:
        console.print(f"[yellow]⚠[/yellow] DB directory does not exist yet: {db_dir}")
        console.print("    (it will be created on first run)")

    # ── Config sanity ────────────────────────────────────────────────────
    if cfg.agent_timeout_seconds < 30:
        console.print(f"[yellow]⚠[/yellow] agent_timeout_seconds ({cfg.agent_timeout_seconds}) is very low")

    console.print(f"[green]✔[/green] Config validated — {cfg.log_level.value} logging, "
                  f"up to {cfg.max_concurrent_agents} concurrent agents")

    if ok:
        console.print("\n[bold green]✓ orchestrator is ready[/bold green]")
    else:
        console.print("\n[bold red]✗ Some checks failed — review warnings above[/bold red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
