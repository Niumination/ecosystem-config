# Design Code-Level Audit Methodology

A systematic methodology for examining a production web application's design quality from the **source code** — not screenshots or browser inspection. Catches CSS variable drift, inline style vs class inconsistency, component duplication, and design token gaps that visual review misses.

## When to Use

- User asks "cek desain website saya" or "investigasi ui/ux keseluruhan"
- Before a design system retrofit (complements the Retrofit Workflow in the main SKILL.md)
- After a major feature is added, to verify design consistency
- As part of a comprehensive codebase audit (Phase 2 of `codebase-audit` skill)

## Setup — Read the Project Structure First

```bash
# Identify file types
find . -type f -not -path './node_modules/*' -not -path './.git/*' -not -path './.next/*' \
  | grep -oE '\.[a-z]+$' | sort | uniq -c | sort -rn | head -15

# Large files
find . -type f -not -path './node_modules/*' -not -path './.git/*' -not -path './.next/*' \
  -exec du -h {} + | sort -rh | head -15
```

## The 8 Checks

### 1. CSS Variable Cross-Reference

Extract every `var(--x)` usage across the codebase and cross-check against `:root` definitions.

**Commands:**

```bash
# All variables USED in .css files + .js/.tsx components
grep -roE 'var\(--[a-z-0-9]+\)' . --include='*.css' --include='*.js' --include='*.tsx' --include='*.vue' \
  2>/dev/null | grep -oE '--[a-z-0-9]+' | sort -u > /tmp/var-used.txt

# All variables DEFINED in :root / [data-theme]
grep -E '^\s+--[a-z-0-9]+:' styles/globals.css main.css 2>/dev/null | sed 's/:.*//;s/^\s*//' | sort -u > /tmp/var-defined.txt

# UNDEFINED variables (render as initial value = invisible bug)
comm -23 /tmp/var-used.txt /tmp/var-defined.txt
```

**Common false positives to check manually:**
- Variables defined inside `<style jsx>` blocks (Next.js) — extract them separately by searching for `:root` or CSS inside `<style jsx>`
- Variables defined in component-level CSS modules

**What it catches:** `--gray-200`, `--white`, `--primary-light` used in old `<style jsx>` components but never defined in the global `:root` — these render as the CSS `initial` value (usually transparent or browser default).

### 2. Design Token Integrity (Dark Mode Coverage)

Verify that every major semantic token has a dark mode override:

```bash
# Check all :root tokens
grep -oE '^\s+--[a-z-]+[a-z]' styles/globals.css 2>/dev/null | sort -u > /tmp/root-vars.txt

# Check data-theme="dark" tokens
awk '/data-theme="dark"/{flag=1;next}/^[^{]/{if(flag && /^[a-zA-Z@.{}]/)flag=0}flag' styles/globals.css \
  2>/dev/null | grep -oE '^\s+--[a-z-]+' | sort -u > /tmp/dark-vars.txt

# Missing from dark mode
comm -23 /tmp/root-vars.txt /tmp/dark-vars.txt
```

**If missing tokens is small** (1–3) — minor gap.
**If moderate** (4–10) — some sections render unreadably in one theme.
**If large** (10+) — dark mode is incomplete.

### 3. Inline Styles vs CSS Class Audit

Find JSX/HTML inline style objects that should be CSS classes:

```bash
# Find inline style objects in JS/TSX files
grep -rn 'style={{\|style={{' pages/ components/ --include='*.js' --include='*.tsx' --include='*.vue' 2>/dev/null | head -40
```

**Categorize each finding:**
- **🟢 Utilitarian** — `flex`, `gap`, `margin`, `padding` in layout components. Acceptable but prefer utility classes.
- **🟡 Design** — `colors`, `shadows`, `borders`, `fontSize`, `fontWeight`, `borderRadius`. Should be CSS classes.
- **🔴 Event-driven** — `onMouseEnter`/`onMouseLeave` setting inline `transform`, `boxShadow`. Should use CSS `:hover`.
- **🟢 Unique one-offs** — Page-specific overrides documented inline. Acceptable.

**Signal strength:** 4+ files with inline design styles = code consistency concern.
**Red flag:** Mouse event handlers duplicating CSS hover behavior across components.

### 4. Component Duplication Detection

Search for structurally similar components implementing the same UI pattern differently:

```bash
# Count files using each layout pattern
grep -rc 'className="card' pages/ components/ 2>/dev/null | grep -v ':0$'
grep -rc 'grid-template-columns\|gridTemplateColumns' pages/ components/ styles/ 2>/dev/null | grep -v ':0$'
grep -rc 'position.*fixed\|position:\s*fixed' pages/ components/ 2>/dev/null | grep -v ':0$'

# Check for dual sidebar implementations
grep -rn 'class.*sidebar\|className.*sidebar' pages/ components/ --include='*.js' --include='*.css' 2>/dev/null | head -20
```

**What to flag:**
- Dual sidebar implementations (CSS grid + position:fixed + JS inline)
- Multiple hero component styles on different pages
- Inconsistent card patterns (some use className, some inline styles)
- Admin/private layout classes that exist but have hidden/empty implementations

### 5. `<style jsx>` vs Global CSS Bifurcation

Components with `<style jsx>` (Next.js) or `<style scoped>` (Vue/Svelte) can drift from the global design system over time:

```bash
# Find scoped style usage
grep -rn '<style jsx\|<style scoped\<style module' . --include='*.js' --include='*.tsx' --include='*.vue' --include='*.svelte' | head -20
```

**Checklist for each scoped block:**
- [ ] Uses `var(--x)` from global tokens, not hardcoded values
- [ ] Variable names match the global `:root` definitions
- [ ] No undefined variable references (see Check 1)
- [ ] Could the component migrate to globals.css?

**If scoped styles use hardcoded colors/fonts:** they will NOT update when the design system changes.

### 6. Empty / Loading / Error State Coverage

Check each data-driven component for complete state coverage:

```bash
# Loading states
grep -nc 'loading\|isLoading\|Loading\.' pages/ components/ --include='*.js' 2>/dev/null | grep -v ':0$'

# Empty states  
grep -nc 'length === 0\|\.length ===\s*0\|no data\|tidak ditemukan\|empty\|noResults\|filtered\.length' pages/ components/ --include='*.js' 2>/dev/null | grep -v ':0$'

# Error states
grep -nc 'error\|catch\|errMsg\|setError\|onError\|try' pages/ components/ --include='*.js' 2>/dev/null | grep -v ':0$'
```

**Categorize data-driven components (those with fetch/loop/map):**
- ✅ Has all 3 states — well-engineered
- ⚠️ Has 1–2 states — gap exists for certain scenarios
- ❌ No states — data shows without any UI feedback for edge cases

**For static JSON data** (no async fetch): loading state is optional, but empty/error states still matter.

### 7. Accessibility & SEO Checklist

**Interactive elements:**
- [ ] **Skip link** — first focusable element, visible on `:focus` or `:focus-visible`
- [ ] **Focus visible** — `:focus-visible` style on all interactive elements (keyboard nav indicator)
- [ ] **Keyboard navigation** — Tab order = visual order, no `tabIndex > 0`
- [ ] **aria-label** — on all icon-only buttons and links
- [ ] **aria-expanded** — on expandable triggers (accordion, dropdown)
- [ ] **Form labels** — `<label htmlFor="..."` or `aria-labelledby` on inputs
- [ ] **Alt text** — `alt` on all `<img>` / `Image` components

**Motion:**
- [ ] **Reduced motion** — `@media (prefers-reduced-motion: reduce)` disables all animations
- [ ] **Stagger reveal** exits gracefully when motion reduced

**Print:**
- [ ] **Print styles** — `@media print` hides chrome (sidebar, topbar, FAB), shows content

**SEO:**
- [ ] **Meta description** — unique `<meta name="description">` per page
- [ ] **Open Graph** — `og:title`, `og:description`, `og:image`, `og:type` per key page
- [ ] **Twitter Cards** — `twitter:card`, `twitter:site`
- [ ] **Canonical URL** — `<link rel="canonical">` on every page
- [ ] **Structured data** — JSON-LD for Organization, WebSite, BreadcrumbList
- [ ] **Page titles** — unique `<title>` per page (format: "Page — Site Name")

### 8. Data Source Flatness Validation

When the dashboard/UI relies on JSON data, verify values aren't accidentally identical across all entries:

```bash
# Check numeric values distribution
python3 -c "
import json, sys

try:
    d = json.load(open(sys.argv[1]))
except:
    d = json.load(open(sys.argv[1]))['data']

# Extract all numeric-like values
nums = []
for item in d if isinstance(d, list) else d.values():
    if isinstance(item, dict):
        for k, v in item.items():
            if isinstance(v, (int, float)):
                nums.append(v)
    elif isinstance(item, (int, float)):
        nums.append(item)

if nums:
    unique = set(nums)
    print(f'Range: {min(nums)} — {max(nums)}')
    print(f'Unique values: {len(unique)} (out of {len(nums)} total)')
    if len(unique) <= 2:
        print(f'⚠️ FLAT DATA: All values {unique}')
    else:
        print(f'✅ Good variation: {sorted(unique)}')
" path/to/data.json
```

**When all values are identical:** The dashboard bars/gauges render uniformly flat — no visible differentiation between categories. Not necessarily a bug (early baseline data is legitimate), but the UX should communicate that this is a starting baseline through labels or annotations.

## Report Format

Present findings as a structured two-section report:

### Section A: Scoreboard

| Aspek | Rating | Notes |
|-------|--------|-------|
| Visual Design | ⭐⭐⭐½ | Brief summary |
| Typography | ⭐⭐⭐⭐ | Brief summary |
| Accessibility | ⭐⭐⭐½ | Key omissions |
| Responsiveness | ⭐⭐⭐⭐ | Breakpoint quality |
| Code Consistency | ⭐⭐⭐ | Dual implementations |
| UX Flow | ⭐⭐⭐⭐ | Navigation, feedback |
| SEO/Optimization | ⭐⭐⭐ | Meta/OG gaps |

**Overall: N/5** — One-sentence verdict.

### Section B: Findings Detail

| # | Area | Severity | Issue | Location | Fix Approach |
|---|------|----------|-------|----------|-------------|
| 1 | CSS | 🟡 Medium | `--gray-200` undefined | `faq.js:122` | Replace with `--line` |
| 2 | Components | 🟡 Medium | Dual sidebar (CSS + JS) | Sidebar.js + globals.css | Consolidate |
| ... | ... | ... | ... | ... | ... |

**Follow-up:** Offer to apply fixes, starting with the highest severity.

## Pitfalls

- **CSS variable cross-reference is non-optional** — undefined vars render as `initial` (often transparent). This is the #1 silent bug in migrated codebases.
- **"It works visually" ≠ "coded cleanly"** — inline styles render correctly but degrade maintainability. Flag patterns (3+ files with similar inline design styles), not individual occurrences.
- **Don't ignore `<style jsx>`** — easy to miss in a globals.css-focused audit. Same applies to Vue `<style scoped>` and Svelte `<style>`.
- **Check BOTH themes** — a component fine in light mode can have invisible text in dark mode due to missing variable overrides.
- **Data flatness ≠ bug** — if all values are 1.0 as a new baseline, it's a **UX communication gap** (dashboard looks undifferentiated), not a bug. Note it as a recommendation, not a defect.
- **Admin/private classes** in CSS but no admin pages in page files = either hidden features or dead CSS. Verify by checking the page directory.
- **Fullstack label vs actual implementation** — if a project claims "fullstack" but has no API routes or server components, flag the label mismatch.
