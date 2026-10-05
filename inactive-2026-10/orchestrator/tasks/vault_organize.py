from .base import Task
from ..utils.vault_state import VaultState
from datetime import datetime
from pathlib import Path

class VaultOrganizeTask(Task):
    name = "vault_organize"
    description = "Organize vault: fix links, clean up, health check"

    def run(self, config):
        log = config.get("_log")
        vault = VaultState(config["vault_root"])
        report = vault.health_report()

        # ── PRINT REPORT ──────────────────────────────────────
        log.info("=" * 56)
        log.info("  VAULT HEALTH REPORT — %s", report["date"])
        log.info("=" * 56)
        log.info("  Stats: %d files, %s",
                 report["stats"]["total_files"],
                 report["stats"]["total_size_mb"])
        log.info("  Folders:")
        for name, count in sorted(report["folders"].items()):
            log.info("    %-20s %d files", name, count)

        fm = report["frontmatter"]
        log.info("  Frontmatter: %d/%d (%s%%)",
                 fm["with_frontmatter"], fm["total"], fm["coverage_pct"])
        if fm["issues"]:
            log.warning("  Frontmatter issues:")
            for i in fm["issues"][:5]:
                log.warning("    ⚠ %s: %s", i["file"], i["issue"])

        bl = report["broken_links"]
        if bl["count"] > 0:
            log.warning("  Broken links: %d", bl["count"])
            for b in bl["items"][:5]:
                log.warning("    %s → [[%s]]", b["source"], b["target"])
        else:
            log.info("  Broken links: none")

        orp = report["orphan_notes"]
        if orp["count"] > 0:
            log.warning("  Orphan notes: %d", orp["count"])
            for o in orp["items"][:5]:
                log.warning("    %s", o)
        else:
            log.info("  Orphan notes: none")

        # ── GENERATE REPORT NOTE ──────────────────────────────
        report_dir = Path(config["vault_root"]) / "01 Updates"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"Vault Health Report - {datetime.now().strftime('%Y-%m-%d')}.md"
        lines = ["---", "type: health-report", f"date: {datetime.now().strftime('%Y-%m-%d')}", "---", "",
                  f"# Vault Health Report — {datetime.now().strftime('%Y-%m-%d')}", "",
                  "## Stats", f"- Total notes: {fm['total']}", f"- Notes with frontmatter: {fm['with_frontmatter']}/{fm['total']} ({fm['coverage_pct']}%)",
                  f"- Broken links: {bl['count']}", f"- Orphan notes: {orp['count']}", "",
                  "## Files by folder", ""]
        for name, count in sorted(report["folders"].items()):
            lines.append(f"- **{name}**: {count} files")
        if bl["items"]:
            lines += ["", "## Broken Links", ""]
            for b in bl["items"]:
                lines.append(f"- `{b['source']}` → `[[{b['target']}]]`")
        if orp["items"]:
            lines += ["", "## Orphan Notes", ""]
            for o in orp["items"]:
                lines.append(f"- `{o}`")
        if fm["issues"]:
            lines += ["", "## Frontmatter Issues", ""]
            for i in fm["issues"]:
                lines.append(f"- `{i['file']}`: {i['issue']}")
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        log.info("  Report saved: %s", report_path.relative_to(config["vault_root"]))

        log.info("=" * 56)
        log.info("✅ Vault health check complete")
        return {"status": "done", "report": report}
