---
name: ui-ux-pro-max
description: "UI/UX design intelligence. 67 styles, 96 palettes, 57 font pairings, 25 charts, 13 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples."
tags: ["ui-ux", "design-system", "frontend", "accessibility", "prototyping"]
---

# UI/UX Pro Max - Design Intelligence

Comprehensive design guide for web and mobile applications. Contains 67 styles, 96 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 13 technology stacks. Searchable database with priority-based recommendations.

## Compatibility: Hermes Agent ✅

This skill is installed and ready to use in the current Hermes profile.

**Skill path:** `$HERMES_HOME/skills/ui-ux-pro-max/`

To run the search scripts from anywhere:

```bash
# Via wrapper (recommended — works from any directory):
$HERMES_HOME/skills/ui-ux-pro-max/scripts/uiux-search "saas dashboard dark" --design-system

# Or directly via Python:
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "query" --design-system
```

> **Note:** The `$HERMES_HOME` env var is set automatically by Hermes Agent. In this session it resolves to: `/Volumes/HermesAgent/HermesAgentUSB/data/profiles/opencode`

---

## When to Apply

Reference these guidelines when:
- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing accessibility requirements

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Accessibility | CRITICAL | `ux` |
| 2 | Touch & Interaction | CRITICAL | `ux` |
| 3 | Performance | HIGH | `ux` |
| 4 | Layout & Responsive | HIGH | `ux` |
| 5 | Typography & Color | MEDIUM | `typography`, `color` |
| 6 | Animation | MEDIUM | `ux` |
| 7 | Style Selection | MEDIUM | `style`, `product` |
| 8 | Charts & Data | LOW | `chart` |

## Quick Reference

### 1. Accessibility (CRITICAL)

- `color-contrast` - Minimum 4.5:1 ratio for normal text
- `focus-states` - Visible focus rings on interactive elements
- `alt-text` - Descriptive alt text for meaningful images
- `aria-labels` - aria-label for icon-only buttons
- `keyboard-nav` - Tab order matches visual order
- `form-labels` - Use label with for attribute

### 2. Touch & Interaction (CRITICAL)

- `touch-target-size` - Minimum 44x44px touch targets
- `hover-vs-tap` - Use click/tap for primary interactions
- `loading-buttons` - Disable button during async operations
- `error-feedback` - Clear error messages near problem
- `cursor-pointer` - Add cursor-pointer to clickable elements

### 3. Performance (HIGH)

- `image-optimization` - Use WebP, srcset, lazy loading
- `reduced-motion` - Check prefers-reduced-motion
- `content-jumping` - Reserve space for async content

### 4. Layout & Responsive (HIGH)

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - Minimum 16px body text on mobile
- `horizontal-scroll` - Ensure content fits viewport width
- `z-index-management` - Define z-index scale (10, 20, 30, 50). ⚠️ `filter: blur()` / `backdrop-filter: blur()` creates a new CSS stacking context — elements inside a filtered parent can NOT escape via `z-index` alone (see Animation > `filter-blur-stacking-context`)

### 5. Typography & Color (MEDIUM)

- `line-height` - Use 1.5-1.75 for body text
- `line-length` - Limit to 65-75 characters per line
- `font-pairing` - Match heading/body font personalities

### 6. Animation (MEDIUM)

- `duration-timing` - Use 150-300ms for micro-interactions
- `transform-performance` - Use transform/opacity, not width/height
- `loading-states` - Skeleton screens or spinners
- `filter-blur-stacking-context` — ⚠️ CSS `filter: blur()` and `backdrop-filter: blur()` create a **new stacking context** on the element they're applied to. This breaks `z-index` for all children: an element inside a blurred parent CANNOT raise above siblings outside the parent, regardless of `z-index` value. Modals, overlays, DetailPanels, or dropdowns that overlap a blurred region MUST be rendered outside the filtered ancestor in the DOM tree. Use a shared state store (Zustand, Context, Redux) to communicate state across the layout boundary.
- _Compose-specific:_ animated NavHost (slide+fade), staggered entrance (AnimatedVisibility + LaunchedEffect), pulsing indicators — see `references/jetpack-compose-ui-polish.md`

### 7. Style Selection (MEDIUM)

- `style-match` - Match style to product type
- `consistency` - Use same style across all pages
- `no-emoji-icons` - Use SVG icons, not emojis

### 8. Charts & Data (LOW)

- `chart-type` - Match chart type to data type
- `color-guidance` - Use accessible color palettes
- `data-table` - Provide table alternative for accessibility

---

## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on user's OS:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## How to Use This Skill

When user requests UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Generate Design System (REQUIRED)

**Always start with `--design-system`** to get comprehensive recommendations with reasoning:

```bash
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This command:
1. Searches 5 domains in parallel (product, style, color, landing, typography)
2. Applies reasoning rules from `ui-reasoning.csv` to select best matches
3. Returns complete design system: pattern, style, colors, typography, effects
4. Includes anti-patterns to avoid

**Example:**
```bash
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System (Master + Overrides Pattern)

To save the design system for hierarchical retrieval across sessions, add `--persist`:

```bash
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-system --persist -p "Project Name"
```

This creates:
- `design-system/MASTER.md` — Global Source of Truth with all design rules
- `design-system/pages/` — Folder for page-specific overrides

**With page-specific override:**
```bash
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

This also creates:
- `design-system/pages/dashboard.md` — Page-specific deviations from Master

**How hierarchical retrieval works:**
1. When building a specific page (e.g., "Checkout"), first check `design-system/pages/checkout.md`
2. If the page file exists, its rules **override** the Master file
3. If not, use `design-system/MASTER.md` exclusively

### Step 3: Supplement with Detailed Searches (as needed)

After getting the design system, use domain searches to get additional details:

```bash
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --domain <domain> [-n <max_results>]
```

**When to use detailed searches:**

| Need | Domain | Example |
|------|--------|---------|
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Alternative fonts | `typography` | `--domain typography "elegant luxury"` |
| Landing structure | `landing` | `--domain landing "hero social-proof"` |

### Step 5: Implement & Apply

After receiving the design system output, apply it to the code:

**For GREENFIELD projects (new UI from scratch):**
- Create the project scaffold first (Vite for React, CLI for framework, etc.)
- Set up the CSS variables from the design system's color palette
- Import the recommended fonts in `index.html`
- Build components with the design system's style rules
- Use SVG icons from a consistent set (Heroicons) — never emojis

**For RETROFIT projects (improve existing UI — see full workflow below):**
- Audit existing code against the design system output
- Replace old theme with new theme variables
- Check each component against the Pre-Delivery Checklist

### Step 6: Build & Verify

Always build and test after applying changes:

```bash
# For React/Vite projects
npm run build

# For simple HTML projects
# (manual check)

# Verify server (if applicable)
curl -s http://127.0.0.1:<port>/api/stats   # → 200 JSON
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/   # → 200
```

**Verification checklist after build:**
- [ ] Build succeeds with zero errors
- [ ] Fonts are properly loaded (DevTools → Computed → font-family)
- [ ] CSS custom properties applied correctly
- [ ] Glass effects visible, not invisible
- [ ] No emoji icons remaining in DOM
- [ ] No layout shift on hover
- [ ] `focus-visible` styles work via keyboard navigation (Tab key)

---

## Retrofit Workflow: Applying Design System to Existing Projects

Use this when the user asks to "improve", "fix", "enhance", or "upgrade" the design of an existing project — as opposed to building from scratch.

### When to Use

- User says "perbaiki desain dashboard ini" / "improve this UI"
- Existing project already has code, but looks outdated/unprofessional
- You have a design system output from `--design-system` and need to apply it

### The 5-Step Audit → Fix → Verify Pipeline

#### Step 1: Read All Source Files

Before making any changes, read every relevant source file:
- `index.html` — for font loading, meta tags, Google Fonts links
- `src/index.css` or main CSS — current theme variables, base styles
- Each component file (`.jsx`, `.tsx`, `.vue`, etc.) — look for emoji icons, inline styles
- `package.json` — check for icon libraries (if none, inline SVG is ideal)

#### Step 2: Generate Design System

```bash
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "<product type> <keywords>" --design-system -p "Project Name"
```

Use the output's **Pattern**, **Colors**, **Typography**, **Key Effects**, and **Avoid** sections as the audit criteria.

#### Step 3: Audit Against the Pre-Delivery Checklist

Check each file against the Pre-Delivery Checklist (see below). The most common anti-patterns in existing projects:

| # | Anti-Pattern | Fix | Effort |
|---|-------------|-----|--------|
| 1 | **Emoji icons** (📝, ✅, ⚠️, 🔍, 🎯, 📋, 🗑️) | Replace with inline SVG (Heroicons) | Medium — find-and-replace per icon |
| 2 | **Wrong font** (Inter used for dashboards) | Switch to Fira Code + Fira Sans for data projects | Low — one HTML change |
| 3 | **No prefers-reduced-motion** | Add CSS media query + disable animations | Low — one CSS addition |
| 4 | **No focus-visible states** | Add CSS for keyboard navigation | Low — one CSS addition |
| 5 | **Basic glassmorphism** (single layer, no border) | Add `::after` gradient border overlay | Low — per element |
| 6 | **Wrong theme colors** (Nous dark `#0a0a0f` instead of OLED `#020617`) | Update CSS custom properties | Medium — per variable |
| 7 | **Inter font for dashboard data** (monospace better for IDs/timestamps) | Use Fira Code for data displays | Low — one CSS change |
| 8 | **Scale transforms on hover** (layout shift) | Use color/border/shadow transitions instead | Low — per element |
| 9 | **Cosmetic-only changes** — only colors/fonts/icons changed without altering layout structure; users say "sama aja" / "looks the same" | Include at least one structural layout change: regroup elements (e.g. 7 columns → 4), redesign card layout, change component hierarchy, rework whitespace | Medium — requires component restructuring |
| 10 | **User-requested redesign vs agent-imposed** — Same visual changes get opposite reactions depending on who initiated. User-initiated = "polished", agent-imposed = "makin hancur" | Always wait for the user to say they want a redesign. If they complain about the current design, offer specific options (e.g. "I could add entrance animations — want me to?"). Let the user say YES first. | Low — process change |
| 11 | **Hardcoded colors breaking dark/light theme** — `color: #333` / `background: white` / `border-color: #e5e7eb` in `<style jsx>` blocks don't respond to CSS variable changes, making text invisible in dark mode or backgrounds wrong | Run `search_files` with pattern `color:\s*(#[0-9a-fA-F]{3,6}|rgba?\(|hsl\(` across all JS/CSS files. Replace with theme variables: `#333`/`#111`/`#1a1a1a` → `var(--ink)`, `#888`/`#999`/`#555`/`#666` → `var(--ink-secondary)`/`var(--muted)`, brand blues like `#1e40af`/`#004098`/`#1d70b8` → `var(--primary)`, `white` → `var(--surface)`, `#e5e7eb`/`#eef0f2` → `var(--line)`, `#f0f4ff`/`#eff6ff`/`#e8edf5` → `var(--primary-50)`. Build verify after each batch. See `references/theme-color-audit.md`. | Medium — search per file |

#### Step 4: Apply Changes Systematically

Work in this order to minimize rework:

1. **`index.html`** — update font links (Google Fonts), add meta tags
2. **CSS files** — replace theme variables, add reduced-motion + focus-visible CSS, add glass effects
3. **Components with emoji → SVG** — replace each emoji with its Heroicons equivalent
   - Use inline SVG only (no external icon library)
   - Wrap each SVG in a `shrink-0` container to prevent layout shift on flex layouts
   - Verify each replacement preserves the original icon meaning
4. **Fix interaction** — add `cursor-pointer`, hover transitions, stable hover states
5. **Verify glass elements** — check visibility in both dark and light modes

**Key rule:** Replace emoji icons one-at-a-time. Use a lookup table to map the original emoji to its Heroicons SVG path:

| Emoji | Heroicon Name | Path Pattern |
|-------|--------------|--------------|
| `📝` | Pencil | `M15.232 5.232l...` |
| `✅` | CheckCircle | `M9 12l2 2 4-4m6 2a9 9...` |
| `⚠️` | WarningTriangle | `M12 9v4m0 4h.01M3.5 20.5...` |
| `🔍` | MagnifyingGlass | `M21 21l-6-6m2-5a7 7...` |
| `🎯` | Target | `M12 2a10 10...` |
| `📋` | Document | `M9 12h6M9 16h6M9 8h6M4 4...` |
| `🚀` | Rocket | (use ArrowRight or external link icon instead) |
| `✓` | Check | Same as CheckCircle but minimal |
| `🗑️` | Trash | `M19 7l-.867 12.142A2 2...` |

Heroicons source: https://heroicons.com — use the outline set (`stroke="currentColor"`, `fill="none"`, `strokeWidth="2"`, `viewBox="0 0 24 24"`).

#### Step 5: Build, Run, Verify

```bash
npm run build
node server.js  # or equivalent
```

- Check browser console for zero errors
- Verify fonts loaded correctly
- Check focus-visible by Tab-key navigation
- Confirm glass effects visible
- Confirm no emoji visible in rendered UI

## Common Pitfalls in Retrofit

- **Cosmetic-only changes feel invisible** — Changing colors, fonts, and icons without altering the layout *structure* (column count, card design, whitespace, visual hierarchy) makes the UI look identical to its previous version. Users will say "sama aja" / "looks the same". Always include at least ONE structural layout change.
- **⚠️ The opposite extreme: Over-engineering without permission** — Just as dangerous as cosmetic-only changes. Applying structural changes (column regrouping, glass effects, glow hovers, gradient accents) **without user confirmation** will feel like your UI is "makin hancur" (worse/broken), especially for data-heavy workflow tools where familiarity and clarity matter more than visual flair. **Always get user buy-in before making structural layout changes.** Propose the change, show the rationale, wait for approval.
- **✅ The sweet spot: User-requested animated polish** — When the user explicitly asks for a redesign (as opposed to the agent proposing one), the reception is completely different. The same changes that were rejected as "makin hancur" when agent-initiated are received as "polished" when user-requested. Key conditions for success: (1) preserve layout structure (don't regroup columns or change the page skeleton), (2) apply entrance-only animations (fire once on mount, then UI stays static — no distracting hover glows), (3) stagger delays to communicate hierarchy, (4) respect `prefers-reduced-motion`. See the retrofit case study v3.1 for the full worked example.
- **Design System pattern mismatch** — The `--design-system` output predicts a **Pattern** (e.g. "Portfolio Grid", "Card List", "Showcase"). This pattern may NOT match the actual product type. A kanban project management dashboard is NOT a portfolio grid. If the pattern doesn't conceptually match what you're building, don't blindly apply it. The pattern guides layout structure — using the wrong pattern leads to the wrong layout.
- **Kanban/workflow dashboard constraints** — For kanban boards specifically, these design choices harm usability:
  - Glassmorphism columns (`backdrop-filter: blur`) reduce text readability and scanning speed
  - Glow hover on cards draws attention away from task content (title, status, assignee)
  - Column regrouping (e.g. 7 statuses → 4 groups) without user request destroys mental model
  - Gradient decorative bars on columns add visual noise, not value
  - **Rule of thumb for kanban: clarity > decoration. Users need to scan tasks, not admire columns.**

- **Desktop app getting web landing pattern** — A Tauri/Electron provider-config tool queried with "desktop app dashboard" can return "App Store Style Landing" (hero + device mockup + download CTAs). That pattern is for marketing pages, not dense configuration interfaces. Desktop tools need structural clarity: short list views, inline edit affordances, stable scan paths, minimal motion. **Verify**: if `--design-system` returns Portfolio Grid / Showcase / App Store / Landing Page, discard it and map the product to a data-tool pattern instead.

## Pre-Delivery Checklist

> **Real-world case study — three paths documented:** See `references/retrofit-kanban-dashboard-case-study.md` covering v2.0 (cosmetic-only → "sama aja"), v2.1 (over-engineered → "makin hancur"), the rollback that stabilized things, AND the successful v3.1 user-requested redesign with entrance animations. The v3.1 chapter is the most instructive — it documents what conditions made a redesign succeed after two failures.

> **PNG/icon-font icons** are not emojis — don't replace them. Only replace Unicode emoji characters (`📝`, `✅`, `⚠️`, etc.)

- **Emoji in user-generated content** (task descriptions, comments) should NOT be replaced — only emoji used as functional UI icons
- Some components may use `span` or `div` wrappers around emoji that need SVG-compatible class names (`shrink-0`)
- After SVG replacement, verify icon alignment in flex/grid layouts — inline SVGs may need `flex items-center` on parent
- Build before-and-after: always run a build before changes to confirm it works, then after to confirm nothing broke

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | Page structure, CTA strategies | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel, pie |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | Web interface guidelines | aria, focus, keyboard, semantic, virtualize |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Available Stacks

| Stack | Focus |
|-------|-------|
| `html-tailwind` | Tailwind utilities, responsive, a11y (DEFAULT) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |
| `shadcn` | shadcn/ui components, theming, forms, patterns |
| `jetpack-compose` | Composables, Modifiers, State Hoisting, Recomposition | See `references/jetpack-compose-ui-polish.md` for animated NavHost, custom theme, splash screen, staggered entrance patterns.

---

## Example Workflow

**User request:** "Buat landing page untuk klinik skincare"

### Step 1: Analyze Requirements
- Product type: Beauty/Spa service
- Style keywords: elegant, professional, soft
- Industry: Beauty/Wellness
- Stack: html-tailwind (default)

### Step 2: Generate Design System (REQUIRED)

```bash
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "beauty spa wellness service elegant" --design-system -p "Klinik Sehati"
```

**Output:** Complete design system with pattern, style, colors, typography, effects, and anti-patterns.

### Step 3: Supplement with Detailed Searches (as needed)

```bash
# Get UX guidelines for animation and accessibility
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "animation accessibility" --domain ux

# Get alternative typography options if needed
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "elegant luxury serif" --domain typography
```

### Step 4: Stack Guidelines

```bash
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "layout responsive form" --stack html-tailwind
```

**Then:** Synthesize design system + detailed searches and implement the design.

---

## Output Formats

The `--design-system` flag supports two output formats:

```bash
# ASCII box (default) - best for terminal display
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "fintech crypto" --design-system

# Markdown - best for documentation
python3 "$HERMES_HOME/skills/ui-ux-pro-max/scripts/search.py" "fintech crypto" --design-system -f markdown
```

---

## Tips for Better Results

1. **Be specific with keywords** - "healthcare SaaS dashboard" > "app"
2. **Search multiple times** - Different keywords reveal different insights
3. **Combine domains** - Style + Typography + Color = Complete design system
4. **Always check UX** - Search "animation", "z-index", "accessibility" for common issues
5. **Use stack flag** - Get implementation-specific best practices
6. **Iterate** - If first search doesn't match, try different keywords

---

## Common Rules for Professional UI

These are frequently overlooked issues that make UI look unprofessional:

### Icons & Visual Elements

| Rule | Do | Don't |
|------|----|----- |
| **No emoji icons** | Use SVG icons (Heroicons, Lucide, Simple Icons) | Use emojis like 🎨 🚀 ⚙️ as UI icons |
| **Stable hover states** | Use color/opacity transitions on hover | Use scale transforms that shift layout |
| **Correct brand logos** | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| **Consistent icon sizing** | Use fixed viewBox (24x24) with w-6 h-6 | Mix different icon sizes randomly |

### Interaction & Cursor

| Rule | Do | Don't |
|------|----|----- |
| **Cursor pointer** | Add `cursor-pointer` to all clickable/hoverable cards | Leave default cursor on interactive elements |
| **Hover feedback** | Provide visual feedback (color, shadow, border) | No indication element is interactive |
| **Smooth transitions** | Use `transition-colors duration-200` | Instant state changes or too slow (>500ms) |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|----|----- |
| **Glass card light mode** | Use `bg-white/80` or higher opacity | Use `bg-white/10` (too transparent) |
| **Text contrast light** | Use `#0F172A` (slate-900) for text | Use `#94A3B8` (slate-400) for body text |
| **Muted text light** | Use `#475569` (slate-600) minimum | Use gray-400 or lighter |
| **Border visibility** | Use `border-gray-200` in light mode | Use `border-white/10` (invisible) |

### Layout & Spacing

| Rule | Do | Don't |
|------|----|----- |
| **Floating navbar** | Add `top-4 left-4 right-4` spacing | Stick navbar to `top-0 left-0 right-0` |
| **Content padding** | Account for fixed navbar height | Let content hide behind fixed elements |
| **Consistent max-width** | Use same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

## Dark Nexus / Cyber Dashboard Pattern

For dark cyber dashboards with 3D particle backgrounds, grid overlays, scanlines, and glitch effects, see `references/dark-nexus-theme-pattern.md`. Key assets:
- **CSS template:** `react-three-fiber-nextjs/templates/dark-nexus-theme.css` — ready-to-use stylesheet
- **3D integration:** `react-three-fiber-nextjs` skill — React Three Fiber particle setup in Next.js
- **Color tokens:** Cyan accent (`#00fff2`), magenta secondary (`#b000ff`), red alert (`#ff0040`), green live (`#00ff88`)

## Japanese Zen Studio Pattern

For a warm, nature-inspired dark design system with glassmorphism, matcha/sakura/tokyo neon palette, and 3D origami particles, see `references/japanese-zen-studio-pattern.md`. Key assets:
- **Color palette:** matcha (`#6b8c5e`), sakura (`#e8b4b8`), neon-tokyo (`#7dd3fc`), stone-gray (`#a8a29e`)
- **Tailwind v4 utilities:** `@utility glass`, `glass-card`, `glass-strong`, `glow-matcha`, `glow-sakura`, `status-dot`
- **Atmosphere:** Washi paper noise overlay + vignette (cinematic depth, warm tones instead of cool cyber)
- **3D pattern:** ZenParticles + OrigamiGeometry + CursorLight with auto-performance degradation
- **Interactive card:** `FloatingCard` with tilt + spotlight via Framer Motion
- **Typography:** Inter + JetBrains Mono + Noto Sans JP (Japanese support)
- **Integration guide:** Full workflow for applying Zen overhaul to an existing Next.js project
- **Animation DNA:** Custom `ease-zen` cubic-bezier with staggered entrances, spring hovers, page crossfades

---



## Pre-Delivery Checklist

Before delivering UI code, verify these items:

### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Brand logos are correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] Use theme colors directly (bg-primary) not var() wrapper

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode
- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery
- [ ] **No hardcoded hex/rgba colors in component `<style jsx>` blocks** — all colors reference CSS custom properties (`var(--ink)`, `var(--surface)`, `var(--primary)`, etc.)
- [ ] Toggle dark/light and verify every page: no invisible text, no mismatched backgrounds, no unreadable links

### Layout
- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars (⚠️ `filter: blur()` creates stacking context — see Animation > `filter-blur-stacking-context`)
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected

## Design Code-Level Audit Reference

For a systematic methodology to audit a codebase's design quality from source code — covering CSS variable cross-referencing, inline style vs class consistency, component duplication detection, `<style jsx>` vs global CSS variable drift, and accessibility/SEO gap checks — see `references/design-code-audit-methodology.md`.

Use this **before** a design system retrofit (complements the Retrofit Workflow) or whenever the user asks to "cek desain website" / "investigasi ui/ux keseluruhan".
