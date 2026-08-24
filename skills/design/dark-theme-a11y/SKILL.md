---
name: dark-theme-a11y
description: "Accessibility pitfalls specific to dark/glassmorphism themes. Covers CSS variable fallback mismatches, computed style verification, contrast ratio checking for transparent backgrounds, and the :focus/:focus-visible interaction pattern. Use when auditing a11y on dark UIs, fixing contrast issues in glassmorphism, or when computed styles don't match CSS source."
tags:
  - a11y
  - dark-theme
  - glassmorphism
  - css-variables
  - contrast
  - wcag
last_updated: "2026-08-17"
version: 1.0.0
---

# Dark Theme Accessibility Pitfalls

Real bugs found during WCAG 2.1 AA audit of MC dashboard (dark glassmorphism).

## CSS Variable Fallback Mismatch

When updating a CSS variable (e.g. `--text-muted: #7c8ba0`), **every hardcoded fallback in `var()` must be updated too**.

**The trap:** `var(--t3, #64748b)` — if `--t3` is never defined, the fallback `#64748b` is used. Grep for `--text-muted` won't find this because the variable name differs.

**Real bug:** `--text-muted` updated to #7c8ba0 (AA 5.77:1 ✅) but 6 places used `var(--t3, #64748b)` where `--t3` was undefined → fallback #64748b (4.21:1 ❌ FAIL AA).

**Fix pattern:**
1. After updating any CSS variable, grep for ALL fallback values in `var()` referencing old colors
2. Update each fallback individually
3. Verify with computed styles in browser (not just CSS source):
```javascript
const el = document.querySelector('.target');
const color = getComputedStyle(el).color;
// check ACTUAL computed value, not source
```

## Transparent Background Contrast

Dark glassmorphism uses `rgba()` backgrounds over a dark base. Contrast depends on the COMPOSITED color (background透过glass叠加到base), not just the foreground color.

**Fix:** Calculate contrast against the effective composite:
```python
# Effective background = blend(glass_rgba, base_color)
# Then contrast = WCAG_contrast(fg_color, effective_bg)
```

## :focus + :focus-visible Interaction

When overriding `:focus { outline: none; }` (to remove browser default), you MUST add `:focus-visible` as the replacement. Without it, keyboard users lose ALL focus indication.

**Pattern:**
```css
:focus { outline: none; }          /* remove browser default */
:focus-visible {                    /* keyboard-only focus */
  outline: 2px solid var(--cyan);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(0, 240, 255, 0.18);
}
```

## prefers-reduced-motion Kill-Switch

Dark themes often have heavy animations (gradients, glow effects). Always include:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Verification Checklist (dark themes)

1. [ ] `getComputedStyle()` on actual rendered elements (not CSS source)
2. [ ] Contrast ratio ≥4.5:1 for normal text, ≥3:1 for large text/UI
3. [ ] Focus ring visible on keyboard navigation (`:focus-visible`)
4. [ ] `prefers-reduced-motion` respected
5. [ ] All `var()` fallbacks updated when variable changes
6. [ ] ARIA roles on dynamic elements (window managers, launchers)
7. [ ] Heading hierarchy 1→2→3 (no skipped levels)
