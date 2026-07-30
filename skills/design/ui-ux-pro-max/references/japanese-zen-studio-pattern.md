# Japanese Zen Studio Pattern — Niü Dash Dark Zen Aesthetic

A dark zen-inspired design system with Japanese aesthetic (侘寂 wabi-sabi), glassmorphism, 3D origami particles, and matcha/sakura/tokyo neon palette. Designed for project dashboard and creative studio portfolio UIs.

## When to Use

- Building a dark aesthetic dashboard with Japanese/zen inspiration
- Replacing a cyber/neon theme with a calmer, nature-inspired dark palette
- User asks for "Zen", "Japanese", "matcha green", "sakura pink", or "studio" aesthetic
- Applying glassmorphism with warmer, organic tones instead of cold cyan/magenta

## Color Palette

| Token | Hex | Role |
|-------|-----|------|
| `bg-zen` | `#09090b` | Deepest background (near-black with slight warmth) |
| `bg-washi` | `#f5f5f0` | Light mode text / element color (warm paper-white) |
| `matcha` | `#6b8c5e` | Primary accent (matcha green — calm, grounded) |
| `matcha-glow` | `#8fb381` | Matcha highlight / glow (brighter green) |
| `sakura` | `#e8b4b8` | Secondary accent (cherry blossom pink) |
| `sakura-petal` | `#f2d0d3` | Sakura highlight (lighter pink) |
| `neon-tokyo` | `#7dd3fc` | Tech accent / data highlight (sky blue neon) |
| `indigo-zen` | `#4a5d8f` | Deep accent (indigo, for depth and contrast) |
| `stone-gray` | `#a8a29e` | Muted text (warm stone) |
| `ink-black` | `#1c1917` | Card/secondary background (warm dark) |
| `rice-paper` | `#e7e5e4` | Subtle border (warm light) |

**Design rationale:** Unlike cyber themes (cool blue/cyan/purple), the Zen palette uses warm tones — green, pink, warm gray — to evoke nature, calm, and craftsmanship. The high contrast stays accessible (4.5:1+) while feeling organic.

## Utility Classes (Tailwind v4 `@utility`)

### Glass Card
```css
@utility glass {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(16px) saturate(1.2);
  -webkit-backdrop-filter: blur(16px) saturate(1.2);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

@utility glass-strong {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(24px) saturate(1.4);
  -webkit-backdrop-filter: blur(24px) saturate(1.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

@utility glass-card {
  background: rgba(28, 25, 23, 0.6);
  backdrop-filter: blur(20px) saturate(1.3);
  -webkit-backdrop-filter: blur(20px) saturate(1.3);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 0.75rem;
}
```

### Text Effects
```css
@utility text-gradient {
  background: linear-gradient(135deg, var(--color-matcha-glow), var(--color-sakura));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@utility glow-matcha {
  box-shadow: 0 0 10px color-mix(in srgb, var(--color-matcha-glow) 40%, transparent),
              0 0 30px color-mix(in srgb, var(--color-matcha-glow) 20%, transparent);
}

@utility glow-sakura {
  box-shadow: 0 0 10px color-mix(in srgb, var(--color-sakura) 40%, transparent);
}

@utility glow-tokyo {
  box-shadow: 0 0 10px color-mix(in srgb, var(--color-neon-tokyo) 50%, transparent);
}
```

### Status Dots
```css
@utility status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
}

@utility status-active {
  background: var(--color-matcha-glow);
  box-shadow: 0 0 6px color-mix(in srgb, var(--color-matcha-glow) 50%, transparent);
}

@utility status-standby {
  background: var(--color-neon-tokyo);
  box-shadow: 0 0 6px color-mix(in srgb, var(--color-neon-tokyo) 50%, transparent);
}

@utility status-paused {
  background: var(--color-stone-gray);
}
```

## Atmosphere Layers (from back to front)

```
z-0:  3D Canvas — ZenParticles (floating points) + OrigamiGeometry (tetrahedrons) + CursorLight
z-1:  Washi overlay — paper-texture noise (CSS `background-image: url(...)` with 0.03 opacity)
z-2:  Vignette — radial gradient darkening edges (cinematic depth)
z-10: App content — DashboardLayout, Sidebar, Header, content
```

All overlay layers are `pointer-events: none` so interaction passes through.

### Washi Paper Overlay
```css
.washi-overlay {
  position: fixed;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,..."); /* SVG noise pattern */
  mix-blend-mode: overlay;
}
```

### Vignette
```css
.vignette {
  position: fixed;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  background: radial-gradient(
    ellipse 80% 60% at 50% 50%,
    transparent 40%,
    rgba(9, 9, 11, 0.6) 100%
  );
}
```

## Font Stack

| Role | Font | Weight |
|------|------|--------|
| **Body** | Inter | 400, 500, 600 |
| **Monospace/data** | JetBrains Mono | 400, 500 |
| **Japanese support** | Noto Sans JP | 400, 500, 700 |

```tsx
import { Inter, JetBrains_Mono, Noto_Sans_JP } from 'next/font/google'

const inter = Inter({ variable: '--font-inter', subsets: ['latin'] })
const jetbrains = JetBrains_Mono({ variable: '--font-mono', subsets: ['latin'] })
const notojp = Noto_Sans_JP({ variable: '--font-notojp', subsets: ['latin'], weight: ['400', '500', '700'] })
```

## Animation DNA

All motion uses a custom easing curve inspired by natural movement:

```ts
import { Variants, Transition } from 'framer-motion'

export const easeZen = [0.22, 1, 0.36, 1] as const
export const easeSpring = [0.34, 1.56, 0.64, 1] as const
```

Common variants:

- **fadeInUp:** `opacity: [0, 1], y: [24, 0]` — 0.6s, easeZen
- **staggerContainer:** `transition: { staggerChildren: 0.08 }` for list entrance
- **pageTransition:** `opacity: [0, 1]` with 0.3s, crossfade via `AnimatePresence mode="wait"`
- **cardHover:** scale 1.02 + y: -4 with spring back (not scale on hover — use transform only, not layout shift)
- **slideIn:** Sidebar collapse/expand — width 240 ↔ 64 with stagger on icons

## FloatingCard Component Pattern

Interactive glass card with tilt + spotlight effect using Framer Motion:

```tsx
const x = useMotionValue(0.5)
const y = useMotionValue(0.5)
const rotateX = useSpring(useTransform(y, [0, 1], [8, -8]))
const rotateY = useSpring(useTransform(x, [0, 1], [-8, 8]))

// Spotlight: radial gradient follows mouse
const spotlight = useMotionTemplate`radial-gradient(circle at ${x * 100}% ${y * 100}%, rgba(139, 179, 129, 0.08), transparent 60%)`
```

**Key design choices:**
- Scale transforms cause layout shift — use ONLY on hover (not persisted)
- Use `y: -4` instead of `translateY(-4px)` — Framer Motion handles it
- Spotlight is the primary interaction, tilt is subtle (max ±8°)
- Performance: `onPointerMove` with `requestAnimationFrame` throttle on low-end devices

## 3D Atmosphère (React Three Fiber)

Three composable layers for the Canvas:

| Component | Function | Performance Cost |
|-----------|----------|-----------------|
| `ZenParticles` | 120 floating points with gentle wave motion | Low (PointsMaterial) |
| `OrigamiGeometry` | 12 tetrahedrons with edge glow, slow orbit | Medium (individual meshes) |
| `CursorLight` | PointLight tracking mouse — illuminates geometry from cursor angle | Low (one light) |

Performance auto-degradation via Zustand store:
```tsx
type PerformanceMode = 'zen' | 'balanced' | 'minimal'
// 'zen' → all layers, 'balanced' → skip OrigamiGeometry, 'minimal' → no 3D at all
```

Detection: If FPS drops below 30 for 2 consecutive seconds, auto-step down one tier.

## Integration Pattern (New Design Over Existing Project)

When applying a complete Zen theme overhaul to an existing Next.js project:

### Files to Replace
1. **`app/globals.css`** — Full Tailwind v4 override with `@theme` + `@utility` blocks
2. **`app/layout.tsx`** — Font imports + washi/vignette DOM layers
3. **`app/page.tsx`** — Wrap content in `DashboardLayout` (or equivalent zen layout)

### Files to Create
1. **Layout components** — `DashboardLayout`, `Sidebar`, `Header` with glass design
2. **3D components** — `Scene`, `ZenParticles`, `OrigamiGeometry`, `CursorLight`
3. **Store** — Zustand for theme/performance/routing state
4. **Utility** — `cn()` function (clsx + tailwind-merge), motion variants, reusable `FloatingCard`

### Existing Components to Refactor
- **Strip layout chrome** — Remove inline Sidebar/Header/ThemeProvider from SPA-style components; layout chrome comes from the new `DashboardLayout`
- **Switch page routing** — Replace local `useState('dashboard'|'projects'|...)` with Zustand `activeRoute` from the sidebar
- **Update CSS references** — Replace old CSS variables (`--cyan`, `--bg-primary`, etc.) with Tailwind v4 utility classes from the Zen palette

### Dependencies
```json
"framer-motion": "^11",      // animations
"zustand": "^5",             // state management
"clsx": "^2",                // class utilities
"tailwind-merge": "^3",      // Tailwind class merging
"three": "^0.170",           // 3D
"@react-three/fiber": "^9",  // R3F Canvas
"@react-three/drei": "^10",  // R3F helpers (Float, Edges, etc.)
"lucide-react": "^0.400"     // icons
```

## See Also

- `react-three-fiber-nextjs` skill — R3F integration in Next.js (particles, lines, Canvas setup)
- `ui-ux-pro-max` — Retrofit workflow for applying design system to existing projects
- `react-three-fiber-nextjs` `references/dark-nexus-integration.md` — The cyber counterpart to this zen pattern
