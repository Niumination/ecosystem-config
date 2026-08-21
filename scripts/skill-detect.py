#!/usr/bin/env python3
"""
skill-detect.py — Phase 4 autoskills: scan proyek → rekomendasi skill dari bank.

Pola: adoption dari midudev/autoskills (packages/autoskills/lib.ts + skills-map.ts)
Tapi disederhanakan untuk Niumination: 6 mekanisme deteksi → map ke 68 SKILL.md bank.

Usage:
  python3 scripts/skill-detect.py                          # scan cwd
  python3 scripts/skill-detect.py --dir services/cc-acehtengah
  python3 scripts/skill-detect.py --dir services/niu-mission-control --json
  python3 scripts/skill-detect.py --dir /path/proyek --verbose
  python3 scripts/skill-detect.py --list-map               # lihat semua mapping tech→skill
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

# ── Skill registry (dibaca dari skills/INDEX.md + manifest.json jika ada) ──
#   Map: tech keyword → list[(skill_id, domain, alasan)]

SKILL_MAP: list[dict] = [
    # Python / FastAPI / Flask
    {"tech": "fastapi", "skills": ["fastapi-templates", "fastapi-python"], "reason": "FastAPI terdeteksi (pyproject/requirements/import)"},
    {"tech": "flask", "skills": ["flask-api-development"], "reason": "Flask terdeteksi"},
    {"tech": "pytest", "skills": ["python-testing-patterns"], "reason": "pytest terdeteksi (testing Python)"},
    {"tech": "sqlalchemy", "skills": ["flask-api-development"], "reason": "SQLAlchemy terdeteksi"},
    {"tech": "pydantic", "skills": ["fastapi-templates", "fastapi-python"], "reason": "Pydantic terdeteksi"},
    # Frontend / JS / TS / Next.js
    {"tech": "next", "skills": ["impeccable", "ui-ux-pro-max", "frontend-design"], "reason": "Next.js terdeteksi"},
    {"tech": "react", "skills": ["frontend-design", "impeccable"], "reason": "React terdeteksi"},
    {"tech": "vue", "skills": ["frontend-design", "impeccable"], "reason": "Vue terdeteksi"},
    {"tech": "svelte", "skills": ["frontend-design", "impeccable"], "reason": "Svelte terdeteksi"},
    {"tech": "tailwind", "skills": ["impeccable", "ui-ux-pro-max", "dark-theme-a11y"], "reason": "Tailwind CSS terdeteksi"},
    {"tech": "prisma", "skills": ["flask-api-development", "compliance-checklist-dashboard"], "reason": "Prisma ORM terdeteksi"},
    # A11y / SEO / Design
    {"tech": "a11y", "skills": ["accessibility", "web-accessibility-wcag", "dark-theme-a11y"], "reason": "Kebutuhan a11y/WCAG"},
    {"tech": "seo", "skills": ["seo"], "reason": "SEO terdeteksi"},
    # Compliance / Pemdi / Dashboard
    {"tech": "pemdi", "skills": ["compliance-checklist-dashboard", "pemdi-evidence-management", "pemdi-uiux-refinement", "plan-compliance-audit"], "reason": "Pemdi/SPBE/compliance terdeteksi"},
    {"tech": "dashboard", "skills": ["compliance-checklist-dashboard", "web-dashboard-maintenance", "niu-mission-control-ui", "niu-mission-control-ops"], "reason": "Dashboard terdeteksi"},
    {"tech": "mission-control", "skills": ["niu-mission-control-ops", "niu-mission-control-ui", "web-dashboard-maintenance"], "reason": "Mission Control terdeteksi"},
    # Hermes / Ekosistem / Infra
    {"tech": "hermes", "skills": ["hermes-provider-config", "hermes-agent-skill-authoring", "hermes-uiux-technical", "niu-core-governance", "config-history-review"], "reason": "Hermes terdeteksi"},
    {"tech": "telegram", "skills": ["telegram-router-orchestration"], "reason": "Telegram bridge terdeteksi"},
    {"tech": "kanban", "skills": ["kanban-ecosystem-management"], "reason": "Kanban terdeteksi"},
    # Git / quality / writing
    {"tech": "git-destructive", "skills": ["simplify-code", "delegated-output-verification", "verification-before-completion"], "reason": "Git/workflow terdeteksi"},
    # Data / ML
    {"tech": "agent-reach", "skills": ["agent-reach"], "reason": "Kebutuhan internet/research (web, GitHub, YouTube, RSS)"},
]

# Ekstensi → tech hint (seperti autoskills exts bonus)
EXT_MAP: dict[str, list[str]] = {
    ".py": ["pytest", "fastapi"],
    ".tsx": ["next", "react", "tailwind"],
    ".ts": ["next", "react"],
    ".jsx": ["react"],
    ".vue": ["vue"],
    ".svelte": ["svelte"],
}

@dataclass
class Evidence:
    mechanism: str  # package_name | package_regex | config_file | ext | content_regex
    detail: str
    tech: str

@dataclass
class Recommendation:
    skill: str
    domain: str
    reason: str
    evidence: list[Evidence] = field(default_factory=list)
    confidence: str = "medium"  # high | medium | low

# ── Mekanisme deteksi (6 seperti autoskills, urutan prioritas) ──

def _read_text(p: Path, limit: int = 20000) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")[:limit]
    except Exception:
        return ""

def _load_pkg_json(project: Path) -> dict:
    f = project / "package.json"
    if not f.exists():
        return {}
    try:
        return json.loads(_read_text(f, 50000))
    except Exception:
        return {}

def _all_deps(pkg: dict) -> dict:
    deps: dict = {}
    for k in ("dependencies", "devDependencies", "peerDependencies"):
        if isinstance(pkg.get(k), dict):
            deps.update(pkg[k])
    return deps

def _read_pyproject(project: Path) -> str:
    for name in ("pyproject.toml", "requirements.txt", "requirements-dev.txt", "Pipfile", "poetry.lock"):
        f = project / name
        if f.exists():
            return _read_text(f).lower()
    return ""

def detect_project(project: Path, verbose: bool = False) -> tuple[list[Evidence], dict[str, int]]:
    """Jalankan 6 mekanisme, kumpulkan Evidence per tech."""
    evidence: list[Evidence] = []
    tech_hits: dict[str, int] = {}  # tech → score (banyak mekanisme yang hit = lebih yakin)

    def hit(tech: str, mech: str, detail: str):
        evidence.append(Evidence(mech, detail, tech))
        tech_hits[tech] = tech_hits.get(tech, 0) + 1

    pkg = _load_pkg_json(project)
    deps = _all_deps(pkg)
    dep_names_lower = {k.lower(): v for k, v in deps.items()}
    pkg_text_raw = _read_text(project / "package.json").lower()
    py_text = _read_pyproject(project)
    # 1) package names (exact) — package.json deps
    for dep in dep_names_lower:
        # direct match tech
        for m in SKILL_MAP:
            if m["tech"].lower() == dep or m["tech"].lower() in dep:
                # but only if dep name actually contains the tech (e.g. "next" in "next", "@prisma/client" contains prisma)
                pass
        # normalize: check if tech is substring of dep or vice versa
        for m in SKILL_MAP:
            t = m["tech"].lower()
            if t == dep or t in dep or dep in t:
                # avoid false positive: "react" should not hit "react-leaflet" overly? it should — it's react
                if t in ("next", "react", "vue", "svelte", "tailwind", "prisma"):
                    if t in dep:
                        hit(m["tech"], "package_name", f"package.json:{dep}")
                elif t in dep or dep == t:
                    hit(m["tech"], "package_name", f"package.json:{dep}")

    # 1b) Python package names dari pyproject/requirements
    if py_text:
        for m in SKILL_MAP:
            t = m["tech"].lower()
            if t in py_text:
                # ensure word boundary-ish
                if re.search(rf"(^|[^a-z0-9_-]){re.escape(t)}([^a-z0-9_-]|$)", py_text):
                    hit(m["tech"], "package_name", f"py:{t} in pyproject/requirements")

    # 2) package regex — pola nama paket
    #    misal next* , @prisma/*, eslint-*
    if pkg_text_raw:
        for pat, tech in [(r'"next"', "next"), (r'"react\"', "react"), (r'"prisma"', "prisma"), (r'"tailwind', "tailwind")]:
            if re.search(pat, pkg_text_raw):
                hit(tech, "package_regex", f"package.json regex {pat}")

    # 3) config files
    config_map = {
        "next.config.ts": "next", "next.config.js": "next", "next.config.mjs": "next",
        "tailwind.config": "tailwind", "postcss.config": "tailwind",
        "prisma": "prisma",  # folder prisma/ atau schema.prisma
        "pytest.ini": "pytest", "conftest.py": "pytest",
        "vercel.json": "next",
    }
    for name, tech in config_map.items():
        # file exact atau prefix match
        for f in project.iterdir() if project.is_dir() else []:
            if f.name == name or f.name.startswith(name):
                hit(tech, "config_file", str(f.name))
                break
        # nested: prisma/schema.prisma
        if name == "prisma" and (project / "prisma" / "schema.prisma").exists():
            hit("prisma", "config_file", "prisma/schema.prisma")

    # 4) file extensions (scan top-level + src/ + frontend/)
    ext_counts: dict[str, int] = {}
    scan_dirs = [project]
    for sub in ("src", "frontend", "app", "pages", "components"):
        d = project / sub
        if d.is_dir():
            scan_dirs.append(d)
    for d in scan_dirs:
        try:
            for f in d.iterdir():
                if f.is_file() and f.suffix:
                    ext_counts[f.suffix.lower()] = ext_counts.get(f.suffix.lower(), 0) + 1
                if f.is_dir() and d == project:
                    # one level deep: src/**/*.tsx hit by walking
                    try:
                        for g in f.rglob("*"):
                            if g.is_file() and g.suffix:
                                ext_counts[g.suffix.lower()] = ext_counts.get(g.suffix.lower(), 0) + 1
                                if sum(ext_counts.values()) > 500:
                                    break
                    except Exception:
                        pass
        except Exception:
            pass
    for ext, techs in EXT_MAP.items():
        if ext_counts.get(ext, 0) > 0:
            for t in techs:
                hit(t, "ext", f"*{ext} ×{ext_counts[ext]}")

    # 5) content regex — scan isi config untuk tech
    content_checks: list[tuple[str, str, str]] = [
        (r"pemdi|spbe|permempanrb|evidence.*management", "pemdi", "Pemdi/SPBE di codebase"),
        (r"mission.control|mission-control", "mission-control", "Mission Control"),
        (r"hermes|cua-driver|opencode-zen", "hermes", "Hermes di config/code"),
        (r"telegram.*router|niu.*fence|HOOK.*telegram", "telegram", "Telegram bridge"),
        (r"kanban|BACKLOG\.md", "kanban", "Kanban/BACKLOG"),
        (r"prisma\.", "prisma", "prisma. di source"),
        (r"from\s+next|import.*next", "next", "import next di source"),
        (r"content.*pipeline|opendataloader|odl-pdf", "dashboard", "Content pipeline"),
    ]
    # cari di beberapa file representatif
    probe_files = [project / "package.json", project / "AGENTS.md", project / "README.md", project / "next.config.ts"]
    for pf in probe_files:
        if pf.exists():
            txt = _read_text(pf, 10000).lower()
            for pat, tech, desc in content_checks:
                if re.search(pat, txt):
                    hit(tech, "content_regex", f"{pf.name}:{desc}")

    # 6) Gemfile / go.mod / Cargo.toml / composer.json — untuk completeness (phase 1 threshold: warn if found but no mapping)
    for fname in ("Gemfile", "go.mod", "Cargo.toml", "composer.json"):
        if (project / fname).exists():
            hit(fname.split(".")[0].lower(), "config_file", fname)

    return evidence, tech_hits

def resolve_skills(tech_hits: dict[str, int], evidence: list[Evidence]) -> list[Recommendation]:
    """Map tech_hits → skill recommendations (dedup, score confidence)."""
    skill_to_rec: dict[str, Recommendation] = {}
    # domain lookup dari bank
    domain_by_skill: dict[str, str] = {}
    if SKILLS_DIR.exists():
        for domain_dir in SKILLS_DIR.iterdir():
            if not domain_dir.is_dir():
                continue
            for skill_dir in domain_dir.iterdir():
                if (skill_dir / "SKILL.md").exists():
                    domain_by_skill[skill_dir.name] = domain_dir.name

    for m in SKILL_MAP:
        t = m["tech"]
        if t not in tech_hits:
            continue
        hits = tech_hits[t]
        conf = "high" if hits >= 2 else "medium" if hits == 1 else "low"
        evs = [e for e in evidence if e.tech == t]
        for skill_id in m["skills"]:
            if skill_id not in domain_by_skill:
                continue  # skill tidak ada di bank (skip)
            if skill_id in skill_to_rec:
                # merge evidence dedup by (mechanism, detail)
                existing = skill_to_rec[skill_id]
                seen = {(e.mechanism, e.detail) for e in existing.evidence}
                for e in evs:
                    key = (e.mechanism, e.detail)
                    if key not in seen:
                        existing.evidence.append(e)
                        seen.add(key)
                if conf == "high":
                    existing.confidence = "high"
                continue
            skill_to_rec[skill_id] = Recommendation(
                skill=skill_id,
                domain=domain_by_skill.get(skill_id, "unknown"),
                reason=m["reason"],
                evidence=list(evs),
                confidence=conf,
            )
    # bonus: if project has many TSX + next, ensure frontend-design/impeccable ranked high
    return sorted(skill_to_rec.values(), key=lambda r: ({"high": 0, "medium": 1, "low": 2}.get(r.confidence, 2), r.skill))

def scan_project(project: Path, verbose: bool = False) -> dict:
    evidence, tech_hits = detect_project(project, verbose)
    recs = resolve_skills(tech_hits, evidence)
    # workspace/monorepo: scan subdirs dengan package.json sendiri (opsional)
    sub_projects = []
    if project.is_dir():
        for child in project.iterdir():
            if child.is_dir() and (child / "package.json").exists() and child.name not in ("node_modules", ".next", "dist", "build", "out"):
                # only if the parent didn't already strongly match (avoid noise on big repos)
                if child != project:
                    # recurse one level — collect unique skills
                    sub_ev, sub_hits = detect_project(child, False)
                    sub_recs = resolve_skills(sub_hits, sub_ev)
                    if sub_recs:
                        sub_projects.append({"dir": child.name, "skills": [r.skill for r in sub_recs]})

    return {
        "project": str(project),
        "tech_hits": tech_hits,
        "evidence": [{"tech": e.tech, "mechanism": e.mechanism, "detail": e.detail} for e in evidence],
        "recommendations": [
            {"skill": r.skill, "domain": r.domain, "confidence": r.confidence, "reason": r.reason,
             "evidence": [{"mechanism": e.mechanism, "detail": e.detail} for e in r.evidence]}
            for r in recs
        ],
        "subProjects": sub_projects,
    }

def format_human(result: dict, verbose: bool = False) -> str:
    lines: list[str] = []
    lines.append(f"📦 Proyek: {result['project']}")
    if result["tech_hits"]:
        hits_str = ", ".join(f"{k}×{v}" for k, v in sorted(result["tech_hits"].items(), key=lambda x: -x[1]))
        lines.append(f"🔍 Tech: {hits_str}")
    else:
        lines.append("🔍 Tech: (tidak ada yang terdeteksi — coba --verbose)")
    recs = result["recommendations"]
    if not recs:
        lines.append("\n(tidak ada skill yang direkomendasikan)")
        return "\n".join(lines)
    lines.append(f"\n✨ Rekomendasi {len(recs)} skill dari bank ({SKILLS_DIR}):")
    for r in recs:
        badge = {"high": "●", "medium": "◐", "low": "○"}.get(r["confidence"], "○")
        lines.append(f"  {badge} [{r['confidence']}] {r['skill']} ({r['domain']}) — {r['reason']}")
        if verbose:
            for e in r["evidence"]:
                lines.append(f"      ↳ {e['mechanism']}: {e['detail']}")
        else:
            # ringkas: satu baris evidence
            ev_str = ", ".join(f"{e['mechanism']}:{e['detail']}" for e in r["evidence"][:3])
            if ev_str:
                lines.append(f"      ↳ {ev_str}")
    if result["subProjects"]:
        lines.append("\n📁 Sub-proyek terdeteksi:")
        for sp in result["subProjects"]:
            lines.append(f"  - {sp['dir']}: {', '.join(sp['skills'])}")
    lines.append(f"\n💡 Pakai: bash skills/sync-to-agents.sh  (sync)  atau baca skills/<domain>/<skill>/SKILL.md")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="skill-detect — Phase 4: scan repo → rekomendasi skill bank")
    ap.add_argument("--dir", default=".", help="direktori proyek yang di-scan (default: .)")
    ap.add_argument("--json", action="store_true", help="output JSON (untuk tooling)")
    ap.add_argument("--verbose", action="store_true", help="tampilkan semua evidence")
    ap.add_argument("--list-map", action="store_true", help="tampilkan pemetaan tech→skill")
    args = ap.parse_args()

    if args.list_map:
        print(f"{'Tech':<18} {'Skill(s)':<60} Reason")
        print("-" * 120)
        for m in SKILL_MAP:
            print(f"{m['tech']:<18} {', '.join(m['skills']):<60} {m['reason']}")
        return 0

    project = Path(args.dir).resolve()
    if not project.exists():
        print(f"Direktori tidak ada: {project}", file=sys.stderr)
        return 2

    result = scan_project(project, verbose=args.verbose)

    if args.json:
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print(format_human(result, verbose=args.verbose))
        if not result["recommendations"]:
            print("\nTip: --verbose untuk lihat evidence mentah, --json untuk integrasi tooling.", file=sys.stderr)

    return 0

if __name__ == "__main__":
    sys.exit(main())
