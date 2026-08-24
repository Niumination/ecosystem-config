---
name: web-dashboard-maintenance
description: "Maintenance patterns for unified dashboards (Mission Control) using template-based generation."
---

# Web UI & Dashboard Integration Pitfalls

This skill captures non-obvious patterns for maintaining unified dashboards (like Mission Control) where JS is generated from Python/f-strings or HTML template literals.

## Troubleshooting Patterns

- **IIFE Template Integration**: When injecting UI components or JS functions into a unified HTML dashboard, always define functions inside the main IIFE to maintain scope access (PAGES, mount, etc.). Avoid injecting functions between the IIFE closing (`}());`) and the end of the script block, as this breaks scope and access to state objects.
- **Backtick Escaping**: When building strings for `innerHTML` using template literals, especially inside Python f-strings or dynamically generated JS, ensure that nested expressions and backticks are properly balanced. Even-numbered backticks are mandatory; if they become odd-numbered, check for missing/extra closings before `join('')` or `map()`.
- **API Response Sync**: When adding new router endpoints (e.g., `audit.py`), always update the corresponding frontend JS parser (e.g., `app.js` or `build_unified.py` logic) to match the new response schema. Missing properties (like `memory.percent` or `cost.breakdown`) cause runtime `TypeError: Cannot read properties of undefined` in the UI. Always probe existing schema with `curl` before and after updating the backend.