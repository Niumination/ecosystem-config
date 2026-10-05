import os
import re
from datetime import datetime
from pathlib import Path

class VaultState:
    def __init__(self, vault_root):
        self.root = Path(vault_root).resolve()
        self.exclude_dirs = {".obsidian", ".git", "__pycache__", ".DS_Store", "logs"}

    def _walk_md(self):
        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in self.exclude_dirs]
            for f in files:
                if f.endswith(".md"):
                    yield Path(root) / f

    def scan(self):
        folders = []
        files = []
        for entry in sorted(self.root.iterdir()):
            if entry.name.startswith(".") or entry.name in self.exclude_dirs:
                continue
            if entry.is_dir():
                folders.append({
                    "name": entry.name,
                    "path": str(entry.relative_to(self.root)),
                    "file_count": len([f for f in entry.rglob("*") if f.is_file() and not f.name.startswith(".")])
                })
            elif entry.is_file():
                files.append({
                    "name": entry.name,
                    "path": str(entry.relative_to(self.root)),
                    "size_kb": round(entry.stat().st_size / 1024, 1)
                })
        return {"folders": folders, "files": files}

    def get_stats(self):
        total_files = 0
        total_size = 0
        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in self.exclude_dirs]
            for f in files:
                if f.startswith("."):
                    continue
                total_files += 1
                fp = Path(root) / f
                total_size += fp.stat().st_size
        return {
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "last_scan": datetime.now().isoformat()
        }

    def get_unprocessed(self, source_dirs):
        items = []
        for rel in source_dirs:
            src = self.root / rel
            if not src.exists():
                continue
            for entry in sorted(src.iterdir()):
                if entry.is_file() and not entry.name.startswith("."):
                    items.append({
                        "name": entry.name,
                        "path": str(entry),
                        "ext": entry.suffix,
                        "size_kb": round(entry.stat().st_size / 1024, 1)
                    })
        return items

    # ─── LINK ANALYSIS ────────────────────────────────────────────

    WIKILINK_RE = re.compile(r"\[\[([^\]]+?)\]\]")

    def find_all_wikilinks(self):
        links = {}
        for fp in self._walk_md():
            text = fp.read_text(errors="replace")
            rel = str(fp.relative_to(self.root))
            found = self.WIKILINK_RE.findall(text)
            parsed = []
            for raw in found:
                target = raw.split("|")[0].split("#")[0].strip()
                if target:
                    parsed.append({"raw": raw, "target": target})
            if parsed:
                links[rel] = parsed
        return links

    def find_broken_links(self):
        all_md = {f.stem for f in self._walk_md()}
        broken = []
        for rel, refs in self.find_all_wikilinks().items():
            for ref in refs:
                if ref["target"] not in all_md:
                    broken.append({"source": rel, "target": ref["target"], "raw": ref["raw"]})
        return broken

    # ─── ORPHAN ANALYSIS ──────────────────────────────────────────

    def find_orphan_notes(self, exclude={"Welcome.md"}):
        all_md = {}
        for fp in self._walk_md():
            rel = str(fp.relative_to(self.root))
            if rel in exclude:
                continue
            all_md[rel] = fp
        referenced = set()
        for rel, refs in self.find_all_wikilinks().items():
            for ref in refs:
                referenced.add(ref["target"] + ".md")
        orphans = []
        for rel, fp in all_md.items():
            stem = Path(rel).stem
            if stem not in referenced and stem + ".md" not in referenced:
                orphans.append(rel)
        return sorted(orphans)

    # ─── FRONTMATTER ANALYSIS ─────────────────────────────────────

    def parse_frontmatter(self, text):
        text = text.lstrip("\ufeff")
        if not text.startswith("---"):
            return None, None, text
        end = text.find("---", 3)
        if end == -1:
            return None, None, text
        fm_text = text[3:end].strip()
        body = text[end + 3:]
        fm = {}
        valid = True
        for line in fm_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.strip()
                val = val.strip()
                if val.startswith("[") and val.endswith("]"):
                    val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
                elif val.lower() in ("true", "false"):
                    val = val.lower() == "true"
                elif val.isdigit():
                    val = int(val)
                else:
                    val = val.strip('"').strip("'")
                fm[key] = val
            else:
                valid = False
        return fm, valid, body

    def validate_frontmatter(self):
        issues = []
        stats = {"total": 0, "with_fm": 0, "valid_yaml": 0}
        for fp in self._walk_md():
            stats["total"] += 1
            rel = str(fp.relative_to(self.root))
            text = fp.read_text(errors="replace")
            fm, valid, _ = self.parse_frontmatter(text)
            if fm is None:
                if text.startswith("---"):
                    issues.append({"file": rel, "issue": "Malformed frontmatter (no closing ---)"})
                else:
                    issues.append({"file": rel, "issue": "Missing frontmatter"})
            else:
                stats["with_fm"] += 1
                if valid:
                    stats["valid_yaml"] += 1
                else:
                    issues.append({"file": rel, "issue": "Frontmatter has unparseable lines"})
        return stats, issues

    # ─── HEALTH REPORT ────────────────────────────────────────────

    def health_report(self):
        stats = self.get_stats()
        fm_stats, fm_issues = self.validate_frontmatter()
        broken = self.find_broken_links()
        orphans = self.find_orphan_notes()
        structure = self.scan()
        folders_detail = {f["name"]: f["file_count"] for f in structure["folders"]}
        report = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "stats": stats,
            "frontmatter": {
                "total": fm_stats["total"],
                "with_frontmatter": fm_stats["with_fm"],
                "coverage_pct": round(fm_stats["with_fm"] / max(fm_stats["total"], 1) * 100, 1),
                "issues": fm_issues
            },
            "broken_links": {
                "count": len(broken),
                "items": broken
            },
            "orphan_notes": {
                "count": len(orphans),
                "items": orphans
            },
            "folders": folders_detail
        }
        return report
