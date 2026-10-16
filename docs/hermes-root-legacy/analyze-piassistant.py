#!/usr/bin/env python3
"""
Git clone and analyze PiAssistant repository for SoloHost migration.
"""
import subprocess
import os
from pathlib import Path

REPO_URL = "https://github.com/Niumination/VirtualAssistance.git"
DEST_DIR = Path.home() / "SoloHostApps" / "piassistant-local"

print("=== PiAssistant SoloHost Migration Prep ===\n")

# Create destination directory
DEST_DIR.mkdir(parents=True, exist_ok=True)
print(f"📁 Destination: {DEST_DIR}")

# Check if already cloned
if (DEST_DIR / ".git").exists():
    print("✅ Repository already cloned")
else:
    print("📥 Cloning repository...")
    result = subprocess.run(
        ["git", "clone", REPO_URL, str(DEST_DIR)],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Clone successful")
    else:
        print(f"❌ Clone failed: {result.stderr}")
        exit(1)

# Analyze structure
print("\n📊 Repository Analysis:")
print("-" * 50)

# List top-level files
print("\nTop-level files:")
for item in sorted(DEST_DIR.iterdir()):
    if item.is_file():
        print(f"  📄 {item.name}")
    elif item.is_dir() and not item.name.startswith('.'):
        print(f"  📁 {item.name}/")

# Count files by type
ext_count = {}
for file in DEST_DIR.rglob("*"):
    if file.is_file():
        ext = file.suffix.lower() or "(no extension)"
        ext_count[ext] = ext_count.get(ext, 0) + 1

print(f"\nFile types:")
for ext, count in sorted(ext_count.items(), key=lambda x: -x[1])[:10]:
    print(f"  {ext}: {count}")

# Check key files
print(f"\n🔍 Key files check:")
key_files = [
    "package.json",
    "next.config.ts",
    "tsconfig.json",
    "Dockerfile",  # Might not exist yet
    "src/app/page.tsx",
    "src/lib/pi-sdk.ts"
]

for kf in key_files:
    path = DEST_DIR / kf
    if path.exists():
        print(f"  ✅ {kf}")
    else:
        print(f"  ❌ {kf} (missing)")

# Read package.json
print(f"\n📦 Package.json dependencies:")
try:
    import json
    pkg = json.loads((DEST_DIR / "package.json").read_text())
    
    print(f"\n  Name: {pkg.get('name', 'N/A')}")
    print(f"  Version: {pkg.get('version', 'N/A')}")
    print(f"  Scripts: {list(pkg.get('scripts', {}).keys())}")
    
    deps = pkg.get('dependencies', {})
    dev_deps = pkg.get('devDependencies', {})
    
    print(f"\n  Production deps ({len(deps)}):")
    for dep, ver in sorted(deps.items()):
        print(f"    - {dep}: {ver}")
    
    print(f"\n  Dev deps ({len(dev_deps)}):")
    for dep, ver in sorted(dev_deps.items()):
        print(f"    - {dep}: {ver}")
        
except Exception as e:
    print(f"  ⚠️  Could not read package.json: {e}")

print("\n" + "=" * 50)
print("✅ Analysis complete!")
print(f"\nNext steps:")
print(f"  1. cd {DEST_DIR}")
print(f"  2. npm install")
print(f"  3. npm run dev  # Test locally")
print(f"  4. Create Dockerfile for SoloHost")
print(f"  5. Test in Pi Desktop")
