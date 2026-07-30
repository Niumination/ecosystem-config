# Theme Color Audit: Finding & Fixing Hardcoded Colors

Systematic approach to detect hardcoded hex/rgba/hsl colors in component scope that break dark/light theme switching.

## When to Run

- User reports text invisible or unreadable after toggling dark/light theme
- User says "ada teks yang tidak terbaca karena warna text dan background yang sama"
- After a retrofitting design system to an existing project that uses CSS variable theming
- Before delivering any UI with dark/light mode support

## Step 0: Audit CSS Variable Definitions (Reverse Check)

Before fixing hardcoded colors, verify that all CSS variables **referenced** by components actually exist in the stylesheet. A missing variable reference creates invisible text or broken UI even if no hardcoded color exists.

### Find Undefined CSS Variables

Search all source files for `var(--...)` references, then check whether each is defined in the CSS:

```
grep -roh 'var(--[a-zA-Z0-9_-]*' pages/ components/ | sort -u       # used
grep -roh '--[a-zA-Z0-9_-]*:' styles/globals.css | grep -o '--[a-zA-Z0-9_-]*' | sort -u  # defined
```

Cross-reference the two lists. Any variable that appears in the first but not the second must be added.

### Common Missing Variables

Based on real-world audits of Next.js + custom CSS projects:

| Missing Variable | Impact | Typical Fix |
|-----------------|--------|-------------|
| `--gray-100, --gray-200, ..., --gray-900` | Gray text, borders, or backgrounds render as `unset`/transparent | Add shade ramp to both `:root` and `[data-theme="dark"]` |
| `--white` | Backgrounds or text that should be white go transparent | Map to `--surface` in `:root` and `--ink`-adjacent in dark mode |
| `--radius, --radius-lg, --radius-xl` | Border-radius defaults to 0 (sharp corners) | Add uniform radius tokens |
| `--primary-light` | Hover/selected states lose color | Add lighter variant of brand primary |
| `--shadow-sm, --shadow-md, --shadow-lg` | Card/surface depth disappears | Define shadow tokens with `box-shadow` values |

### Dark Mode Variable Matrix

Missing variables must be defined in **both** `:root` (light) and `[data-theme="dark"]` sections. A variable defined only in `:root` silently fails in dark mode (falls back to `unset`, often invisible).

```css
:root {
  --gray-100: #f3f4f6;
  --gray-700: #374151;
}
[data-theme="dark"] {
  --gray-100: #1f2937;   /* dark surface for light gray area */
  --gray-700: #d1d5db;   /* light text on dark background */
}
```

## Step 1: Find All Hardcoded Colors

Use `search_files` with a regex that catches hex, rgb, rgba, and hsl patterns across all source files:

```
search_files(
    pattern=r'color:\s*(#[0-9a-fA-F]{3,6}|rgba?\(|hsl\()',
    file_glob='*.js',
    path='/project/src'
)
```

Also search for `background`, `background-color`, `border-color`, `border`, and `fill` with the same color patterns.

**Key files to scan:**
- All `.js`, `.jsx`, `.tsx`, `.vue`, `.svelte` files (component-scoped `<style jsx>` blocks)
- `.css` files (global styles)
- Any file with inline `style={{ color: '#...' }}` objects

## Step 2: Categorize Each Match

| Category | Action |
|----------|--------|
| **Content colors** (text, bg, borders in page/component content) | Must be replaced with CSS variables |
| **Global theme definitions** (`:root` / `[data-theme]` variable definitions) | Keep — these ARE the variables |
| **Utility/accent colors** (hover states, badges, status indicators) | Replace if they should respond to theme; keep if intentionally static |
| **Sidebar/navbar structural colors** (already use CSS variables) | Skip — already correct |
| **Third-party / library code** | Skip or override via CSS variables externally |

## Step 3: Standard Replacement Map

| Hardcoded Color | CSS Variable | Context |
|----------------|-------------|---------|
| `#333`, `#111`, `#1a1a1a`, `#222` | `var(--ink)` | Primary text |
| `#666`, `#555`, `#888`, `#999` | `var(--ink-secondary)` or `var(--muted)` | Secondary/muted text |
| `#bbb`, `#ccc`, `#ddd` | `var(--muted)` or `var(--muted-200)` | Placeholder, disabled text |
| `white`, `#fff`, `#ffffff` | `var(--surface)` | Card/component backgrounds |
| `#e5e7eb`, `#eef0f2`, `#e2e8f0` | `var(--line)` | Borders, dividers, separators |
| `#f0f4ff`, `#eff6ff`, `#e8edf5` | `var(--primary-50)` | Light primary bg (table rows, highlights) |
| `#004098`, `#1e40af`, `#1d70b8`, `#2563eb` | `var(--primary)` | Primary brand text/accents |
| `#000`, `black` | `var(--ink)` or `var(--overlay)` | Overlays, heavy text |

## Step 4: Apply Changes in Batches

1. **Global CSS first** — ensure theme variables are correctly defined in `:root` / `[data-theme="dark"]`
2. **Common components** (Accordion, Stepper, Card, Button, Banner)
3. **Page-level components** (one page at a time)
4. **Build verify after each batch** — `npm run build && echo "OK"`

## Step 5: Verify

- Toggle dark ↔ light theme
- Check every page for:
  - Invisible text (contrast failure)
  - Mismatched backgrounds (white card on dark mode)
  - Borders that disappear in one mode
  - Links that don't change color with theme

## Pitfalls

- **`filter: blur()` creates a new stacking context** — elements inside a blurred container can't escape via `z-index`. Render modals/overlays outside the filtered parent.
- **`<style jsx>` scope** — CSS variables work inside `<style jsx>` via `var()`, but dynamic styles via `style={{}}` props won't respond to `[data-theme]` selectors unless they reference `var()`.
- **SVG `fill` attributes** — inline SVGs often have hardcoded `fill="#..."` or `stroke="#..."`. Replace with `fill="currentColor"` or reference `var(--ink)`.
- **Don't replace variables in the theme definition file itself** — only replace colors in component files that SHOULD use the variables.
- **Build verify after EVERY batch** — a single bad replacement can break the build. Batch by file group, not all at once.
