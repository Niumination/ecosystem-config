# Retrofit Case Study: Niu-Kanban Dash

## Context

A React 19 + Vite + Tailwind v4 kanban dashboard (7-status columns, Express 5, SQLite backend). Dark OLED theme (#020617), Fira Code + Fira Sans fonts.

This case study documents **four attempts** at redesign — both extremes of the retrofit spectrum, a stable rollback, and finally a successful user-requested redesign with animations.

---

## Attempt 1: v2.0 — Cosmetic-Only (User: "sama aja")

### What Changed

- OLED dark theme (#020617) → ✅
- Fira Code + Fira Sans fonts → ✅
- Emoji icons replaced with SVGs → ✅
- Glassmorphism on header → ✅
- prefers-reduced-motion, focus-visible → ✅

**Result: User saw no visual difference. User feedback: "sama aja — gak ada perubahan signifikan, layout berantakan."**

### Root Cause

The layout structure was untouched — still 7 cramped columns, same card rectangles, same visual hierarchy, same whitespace. Color/font/icon changes alone don't register as a redesign when the layout is identical. Users compare the *shape* of pages, not the hex values.

---

## Attempt 2: v2.1 — Over-Engineered (User: "makin hancur")

### What Changed

Everything. Structural + visual overhaul in one shot:

| Before (v2.0) | After (v2.1) |
|---------------|--------------|
| 7 columns (triage→archived) | 4 grouped columns (Backlog, Active, Blocked, Completed) |
| `grid-cols-7` | `grid-cols-1 md:grid-cols-2 lg:grid-cols-4` |
| Solid card backgrounds | Glass columns with `backdrop-filter: blur(12px)` |
| Minimal cards | Redesigned cards with priority badges, glow hover, assignee avatars |
| Simple header | Gradient purple→cyan header with glow line, stats badges |
| Plain background | Two radial gradient glows at page corners |

### What Went Wrong

1. **No user buy-in for structural changes** — Regrouping 7→4 columns changed the mental model without warning
2. **Glass effects hurt readability** — `backdrop-filter: blur(12px)` on dark columns made task text less crisp. Glass looks great in a portfolio but terrible on a kanban board where scanning speed matters
3. **Glow hover on cards** — distracting, not helpful. Users need to read task titles at a glance, not watch cards glow
4. **Gradient decorative bars** — visual noise with zero functional value on a workflow tool
5. **Too many changes at once** — user couldn't tell which change they didn't like. Everything was different

**Result: User feedback: "makin parah jadinya... kenapa pakai skill ini jadinya makin hancur"**

### Root Cause

The `--design-system` search returned "Portfolio Grid" as the pattern. For a kanban project management dashboard, **Portfolio Grid is not the right pattern**. A portfolio grid focuses on card-level visual presentation (cards as exhibits). A kanban board focuses on workflow, column scanning, and task density. Applying a portfolio grid pattern to a kanban board meant decorating cards and columns instead of optimizing for scanning and clarity.

---

## Attempt 3: Rollback + Minimal Polish (Stable Resolution)

### What Changed

- Layout rolled back to clean **7-column horizontal scroll** (triage, todo, ready, running, blocked, done, archived)
- Solid column backgrounds (`#1a233a`) — no glass, no blur, no gradient accents
- Solid cards — no glow, no gradient, just clean borders with subtle hover transition
- Flat header — gradient text logo (purple→cyan) preserved, but solid `#020617` background, no glow line
- Minimal CSS — no animations except `prefers-reduced-motion`-safe transitions
- OLED dark (#020617), Fira Code/Fira Sans, SVG icons, WCAG focus-visible — all kept

### What Stayed

- Dark OLED theme #020617
- Fira Code + Fira Sans font pair
- Inline SVG icons (Heroicons) — no emoji
- prefers-reduced-motion CSS
- WCAG focus-visible styles
- Cache-Control: no-cache headers in Express server

### Resolution Status

- **User confirmed the layout worked** and was back to a familiar state
- Rollback took effect immediately on `npm run build` + server restart
- Backlog/AGENTS.md were pending revert (user was asked to confirm)

---

## Attempt 4: v3.1 — User-Requested Redesign with Animations (SUCCESS)

### Trigger

User explicitly asked: **"sekarang redesain seluruh tampilan niu kanban dash dengan ui/ux yang lebih proper, aku mau ada beberapa animasi pada tampilan dashboardnya"**

Three key differences from Attempt 2:
1. **User-initiated** — not agent-imposed. The user asked for it.
2. **Animations explicitly requested** — the user wanted motion, not just visual polish.
3. **No structural layout change** — kept 7-column horizontal scroll. Layout was never the complaint; lack of polish was.

### What Changed

#### CSS Foundation (index.css)
- 12 keyframe animations: `fadeInUp`, `slideInLeft`, `slideInRight`, `fadeInDown`, `scaleIn`, `barGrow`, `countUp`, `glowPulse`, `shimmer`, `spin`, `pulse`, `slideDown`
- Animation utility classes for each (`.animate-fade-in-up`, `.animate-slide-in-left`, etc.)
- `prefers-reduced-motion` respected — all animations disabled at `0.01ms`
- `.status-accent` — 3px colored stripe at top of each column
- `.glass-card` — subtle glass on header only (sticky, doesn't affect data density)
- Priority dot glow: `.prio-dot-critical` for P1 items

#### KanbanCard
- **Entrance animation**: `animate-fade-in-up` with `animationDelay: cardIndex * 50ms` — cards enter bottom→up in a wave
- Subtle hover: `-translate-y-0.5` lift + purple box-shadow glow (`0 0 20px rgba(139,108,247,0.08)`)
- Assignee avatar: first-name initial in deterministic-color circle (hash-based palette of 8 colors)
- Critical priority (P1) dot has `glowPulse` animation (red pulsing)
- Relative time format shows "yesterday" for recent items
- `text-decoration: line-through` for done/archived tasks

#### KanbanColumn
- **Entrance animation**: `animate-slide-in-left` with `animationDelay: columnIndex * 70ms` — columns enter left→right in sequence
- Status accent stripe at top (3px, colored per status, 0.6 opacity)
- Better empty state: icon in subtle circle + "No tasks" label
- Header row has subtle hover effect (`bg-white/[0.02]`)

#### Header
- Glass backdrop (`glass-card` class with `backdrop-filter: blur(12px)`) — acceptable because header is sticky, not data-dense
- Logo icon: purple→cyan gradient box with kanban grid SVG
- Stat badges: Total (neutral), Active (purple+dot), Done (green+checkmark) — each in a pill with colored border
- View toggle: gradient background on active, subtle shadow
- Refresh button: rotating arrow SVG when loading, gradient background with hover shadow animation
- Auto-refresh dropdown: `animate-slide-down` entrance, active item prefixed with "●"

#### FilterBar
- **Entrance animation**: `animate-fade-in-down` on mount
- Search input: border + glow shift to purple when active
- Filter pills: gradient background on active, hover states
- Assignee select: custom arrow SVG, custom styling
- Active filter indicator: pulsing purple dot + "filtered" label

#### StatsPanel
- **Staggered entrance**: Each card section enters with `animationDelay` (0ms, 100ms, 200ms, 250ms, 300ms, 350ms)
- Pie chart: `animate-count-up` entrance, hover opacity highlight per slice
- Assignee bars: `animate-bar-grow` with `transform-origin: left` — bars fill from left to right
- Sub-items (status legend, recent done): each has own stagger delay
- Hover border glow per card (purple/cyan/green respectively)

#### Modals (TaskDetail, DoxModal)
- Backdrop: `animate-fade-in`
- Modal panel: `animate-scale-in` (fade + scale 0.95→1 + translateY 8px→0)
- Border radius: `rounded-2xl` (was `rounded-xl`)

### What DIDN'T Change (intentionally)

- **7-column horizontal scroll** — untouched from Attempt 3
- **Column backgrounds** — solid `#0f172a`, no glass/blur on data areas
- **Card backgrounds** — solid `#1a233a`, no glass
- **Data scanning flow** — cards still sorted same way, same info density
- **Server API** — unchanged
- **DB path** — unchanged
- **Font stack** — unchanged (Fira Code + Fira Sans)
- **Theme colors** — unchanged (#020617 primary, etc.)

### What Worked (Analysis)

1. **Layout fidelity → user trust** — Keeping the 7-column layout meant the user saw the same page *shape* they knew. Changes registered as "polished version of my dashboard" not "something new I need to learn"
2. **Animations are entrance-only** — they fire once on mount, then the UI is static. This avoids the "distracting glow" problem of Attempt 2. Motion = alive but not noisy
3. **Animations match kanban workflow** — cards entering bottom→up mimics real tasks appearing; columns sliding left→right matches scan direction
4. **Stagger delays create hierarchy** — columns enter in order (Triage first, Archived last), cards within a column enter by rank. This subtly communicates priority
5. **User asked for it** — critical. The same changes agent-initiated would likely have been rejected as Too Much. User ownership of the request changes reception completely

### Differences from v2.1 (the over-engineered version)

| Aspect | v2.1 (FAIL) | v3.1 (SUCCESS) |
|--------|-------------|-----------------|
| Layout | 7→4 columns (structural) | 7 columns (preserved) |
| Glass | Full-column blur | Header only (sticky, non-data) |
| Animations | Hover glow (distracting) | Entrance only (one-time) |
| Initiation | Agent-initiated | User-requested |
| Changes | Everything at once | One component at a time |
| Pattern applied | Portfolio Grid (wrong) | Custom kanban-aware design |

---

## Key Takeaways

### The Three-Trap Spectrum of Retrofit

```
cosmetic-only          ←→           over-engineered        ←→     user-requested
 ("sama aja")                     ("makin hancur")              (SUCCESS)
      |                                  |                            |
  same layout,                   layout changed without         user owns the ask,
  different colors                 permission + too much         entrance animations,
  → user sees                     → user sees "hancur"           layout preserved
    no difference                                                    → user sees "polished"
```

### Lessons

1. **Generate design system first** — but VERIFY the Pattern matches the actual product type. "Portfolio Grid" ≠ kanban dashboard.
2. **Never apply structural layout changes without user buy-in**. Propose, explain rationale, wait for approval.
3. **Kanban boards: clarity > decoration**. Glassmorphism, glow, and gradient effects reduce scanning speed on data-dense workflow interfaces.
4. **One change at a time** — never push layout restructuring + visual effects + card redesign in a single build. Do one, let user test, get feedback, then the next.
5. **Keep a working backup** — before any retrofit work, know how to roll back (git branch, copy of src/, last build in dist/). This session's rollback took minutes because the original build output was still on disk.
6. **Process to follow for kanban retrofits**:
   a. Read all source files to understand current state
   b. Generate `--design-system` but cross-reference the Pattern with actual product type
   c. If Pattern is wrong, don't apply it — use your own judgment about what layout fits
   d. **Propose structural changes to the user first** — get a "yes" before regrouping columns or redesigning cards
   e. Apply changes one at a time: layout first, then colors/fonts, then effects
   f. Build + verify after EACH change, not all at once
7. **Entrance animations are safe for kanban boards** — they fire once on mount and don't interfere with scanning. Use `animation-delay` with stagger for a polished wave effect.
8. **Wait for the user to ask** — the same redesign agent-initiated vs user-requested gets opposite reactions. Let the user complain first, then offer a paid of options (e.g. "I could add animations — want me to?"). Letting the user say "yes" changes everything.

---

## Design System Output (for reference — from --design-system call)

```
PATTERN: Portfolio Grid           ← MISMATCH! Kanban ≠ Portfolio Grid
STYLE: Dark Mode (OLED)
COLORS: Primary #0F172A, Secondary #1E293B, CTA #22C55E, BG #020617, Text #F8FAFC
TYPOGRAPHY: Fira Code (mono) / Fira Sans (interface)
KEY EFFECTS: Minimal glow, dark-to-light transitions, low white emission
AVOID: Slow updates + No automation
```

**Moral of the story:** The pattern prediction was wrong for this product type. Colors and typography were correct. The key effects and avoid advice was generic. Trust the colors/fonts — question the pattern.

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 18 Jun 2026 | Hermes | v2.0 cosmetic-only → "sama aja" |
| 18 Jun 2026 | Hermes | v2.1 over-engineered → "makin hancur" |
| 18 Jun 2026 | Hermes | Rollback + minimal polish → stable |
| **19 Jun 2026** | **Hermes** | **v3.1 user-requested redesign with animations → SUCCESS** |
