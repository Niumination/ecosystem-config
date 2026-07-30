# Dark Nexus Theme Pattern — Cyber Dashboard Styling

A dark cyber theme with 3D particle background, grid overlay, scanlines, and glitch effects. Designed for project portfolio dashboards and dev tools.

## When to Use

- Building a dark cyber/neon-styled dashboard
- Porting a static HTML cyber dashboard to React
- User asks for "Dark Nexus" or "NIU⚡DASH" style

## Color Palette

| Token | Dark Value | Dim Value | Usage |
|-------|-----------|-----------|-------|
| `--bg-primary` | `#050508` | `#08081a` | Page background |
| `--bg-secondary` | `#0a0a14` | `#0e0e24` | Sidebar/secondary |
| `--bg-card` | `#0d0d1a` | `#12122a` | Card backgrounds |
| `--border` | `#1a1a3a` | `#22224a` | Borders |
| `--cyan` | `#00fff2` | `#00ccbb` | Primary accent |
| `--red` | `#ff0040` | `#cc0040` | Error/alert |
| `--magenta` | `#b000ff` | — | Secondary accent |
| `--green` | `#00ff88` | `#00cc66` | Success/live |
| `--text-primary` | `#e8e8f0` | `#c8c8e0` | Body text |
| `--text-secondary` | `#8888aa` | `#6a6a8a` | Muted text |
| `--text-muted` | `#55557a` | `#4a4a6a` | Subtle text |

## Font Stack

- **Display/Headings:** Orbitron (Google Fonts) — `font-orbitron` class
- **UI/Monospace:** JetBrains Mono (Google Fonts) — `font-mono` class  
- **Body:** Inter (Google Fonts) — default

## Overlay Layers (from back to front)

```
z-0:  3D Canvas / particle background (R3F or vanilla)
z-1:  Grid overlay — animated scrolling cyan grid lines
z-2:  Scanlines — CRT scanline effect
z-3:  Glitch flicker — subtle random opacity glitch
z-10: App content (sidebar, main panel, header)
```

All overlays are `pointer-events: none` so clicks pass through.

## Key CSS Patterns

### Glass Card
```css
.glass {
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}
```

### Text Gradient Logo
```css
.text-gradient {
  background: linear-gradient(135deg, #00fff2, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Active Nav State
```css
.active-nav {
  background: rgba(0, 255, 242, 0.12);
  border-color: var(--cyan);
  box-shadow: inset 0 0 20px rgba(0, 255, 242, 0.06);
}
```

### Live Status Dot
```css
.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 6px rgba(0, 255, 136, 0.5);
}
```

## Theme Toggle (React)

Use a `data-theme` attribute on `<html>` with a React context provider:

```tsx
// ThemeContext with toggleTheme()
const next = theme === 'dark' ? 'dim' : 'dark'
document.documentElement.setAttribute('data-theme', next)
localStorage.setItem('niu-dash-theme', next)
```

CSS automatically switches because: `[data-theme='dim'] { --cyan: #00ccbb; }`

## See Also

- `react-three-fiber-nextjs` skill — R3F 3D particle system integration in Next.js
- `templates/dark-nexus-theme.css` in that skill — full CSS template
