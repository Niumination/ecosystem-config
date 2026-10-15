#!/usr/bin/env python3
"""Validate SoloHost app package before submission."""
import json
import os
import sys
from pathlib import Path

def check_file(path, required=True):
    exists = path.exists()
    if required and not exists:
        print(f"❌ MISSING: {path}")
        return False
    elif not exists:
        print(f"⚠️  OPTIONAL: {path} not found")
        return True
    else:
        print(f"✅ {path}")
        return True

def check_directory(path):
    if path.exists() and path.is_dir():
        print(f"✅ {path}/ (directory)")
        return True
    else:
        print(f"⚠️  {path}/ not found (optional)")
        return True

def validate_manifest(manifest_path):
    """Validate manifest.json structure."""
    print(f"\n=== Validating {manifest_path} ===")
    
    if not manifest_path.exists():
        print("❌ manifest.json not found")
        return False
    
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    
    required_fields = ['version', 'name', 'description', 'author', 'containers']
    missing = [f for f in required_fields if f not in manifest]
    
    if missing:
        print(f"❌ Missing required fields: {missing}")
        return False
    
    print(f"✅ Version: {manifest.get('version')}")
    print(f"✅ Name: {manifest.get('name')}")
    print(f"✅ Author: {manifest.get('author')}")
    
    # Check containers
    containers = manifest.get('containers', [])
    if not containers:
        print("❌ No containers defined")
        return False
    
    for i, container in enumerate(containers):
        print(f"\n  Container {i+1}: {container.get('name', 'unnamed')}")
        
        if 'image' not in container:
            print(f"    ❌ Missing 'image' field")
            return False
        else:
            print(f"    ✅ Image: {container['image']}")
        
        if 'ports' in container:
            for port in container['ports']:
                if 'container' not in port or 'host' not in port:
                    print(f"    ❌ Invalid port mapping: {port}")
                    return False
                else:
                    print(f"    ✅ Port: {port['host']}:{port['container']}")
        
        if 'volumes' in container:
            for vol in container['volumes']:
                if 'name' not in vol or 'path' not in vol:
                    print(f"    ❌ Invalid volume: {vol}")
                    return False
                else:
                    print(f"    ✅ Volume: {vol['name']} -> {vol['path']}")
    
    # Check permissions
    permissions = manifest.get('permissions', {})
    if permissions:
        print(f"\n  Permissions:")
        for key, value in permissions.items():
            print(f"    {key}: {value}")
    
    return True

def validate_dockerfile(dockerfile_path):
    """Check Dockerfile basic requirements."""
    print(f"\n=== Validating {dockerfile_path} ===")
    
    if not dockerfile_path.exists():
        print("❌ Dockerfile not found")
        return False
    
    content = dockerfile_path.read_text()
    
    # Check for essential elements
    checks = [
        ('FROM', 'Base image'),
        ('EXPOSE', 'Port exposure'),
        ('CMD', 'Start command'),
    ]
    
    for keyword, description in checks:
        if keyword in content:
            print(f"✅ {description}: Found")
        else:
            print(f"⚠️  {description}: Not found (may be optional)")
    
    # Check for HEALTHCHECK
    if 'HEALTHCHECK' in content:
        print("✅ HEALTHCHECK: Defined")
    else:
        print("⚠️  HEALTHCHECK: Not defined (recommended)")
    
    return True

def validate_assets(assets_dir):
    """Check for required assets."""
    print(f"\n=== Validating Assets ===")
    
    icon = assets_dir / 'icon.png'
    screenshot = assets_dir / 'screenshot.png'
    
    if icon.exists():
        size = icon.stat().st_size
        print(f"✅ icon.png: {size/1024:.1f} KB")
        
        # Check minimum size (512x512 @ 3bytes/pixel ≈ 750KB)
        if size < 500_000:
            print("  ⚠️  Icon may be too small (recommend 512x512)")
    else:
        print("⚠️  icon.png not found (recommended)")
    
    if screenshot.exists():
        size = screenshot.stat().st_size
        print(f"✅ screenshot.png: {size/1024:.1f} KB")
    else:
        print("⚠️  screenshot.png not found (recommended)")

def validate_readme(readme_path):
    """Check README completeness."""
    print(f"\n=== Validating README ===")
    
    if not readme_path.exists():
        print("❌ README.md not found")
        return False
    
    content = readme_path.read_text()
    lines = content.split('\n')
    
    print(f"✅ README.md: {len(lines)} lines")
    
    # Check for essential sections
    sections = ['## Installation', '## Usage', '## Features']
    for section in sections:
        if section in content:
            print(f"✅ Section found: {section}")
        else:
            print(f"⚠️  Section missing: {section} (recommended)")
    
    return True

def main():
    """Main validation workflow."""
    print("=== SoloHost App Validator ===\n")
    
    # Get app directory
    if len(sys.argv) > 1:
        app_dir = Path(sys.argv[1])
    else:
        app_dir = Path.cwd()
    
    if not app_dir.exists():
        print(f"❌ Directory not found: {app_dir}")
        sys.exit(1)
    
    print(f"Validating: {app_dir}\n")
    
    # Check required files
    print("=== Required Files ===")
    required_files = [
        app_dir / 'Dockerfile',
        app_dir / 'manifest.json',
        app_dir / 'README.md',
    ]
    
    for f in required_files:
        check_file(f, required=True)
    
    # Check optional directories
    print("\n=== Optional Directories ===")
    check_directory(app_dir / 'src')
    check_directory(app_dir / 'assets')
    check_directory(app_dir / 'docs')
    
    # Validate manifest
    manifest_valid = validate_manifest(app_dir / 'manifest.json')
    
    # Validate Dockerfile
    dockerfile_valid = validate_dockerfile(app_dir / 'Dockerfile')
    
    # Validate assets
    validate_assets(app_dir / 'assets')
    
    # Validate README
    readme_valid = validate_readme(app_dir / 'README.md')
    
    # Summary
    print("\n=== Summary ===")
    all_valid = manifest_valid and dockerfile_valid and readme_valid
    
    if all_valid:
        print("✅ All validations passed!")
        print("\nNext steps:")
        print("  1. Build: docker build -t your-app:latest .")
        print("  2. Test: docker run -p 8080:8080 your-app:latest")
        print("  3. Install: Pi Desktop → SoloHost → Install from Local")
        sys.exit(0)
    else:
        print("❌ Some validations failed. Please fix issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
