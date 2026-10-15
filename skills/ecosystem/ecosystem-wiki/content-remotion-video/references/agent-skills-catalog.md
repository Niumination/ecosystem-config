# Remotion Agent Skills Catalog

Installed via `npx remotion skills add` into `.agents/skills/`. Symlinked to Hermes Agent + Qwen Code.

| Skill | What it covers |
|---|---|
| `remotion-best-practices` | Architecture, performance, composition patterns |
| `remotion-captions` | Subtitle rendering, caption animation |
| `remotion-create` | Project scaffolding, template selection |
| `remotion-docs` | Search Remotion documentation |
| `remotion-interactivity` | Player embedding, runtime controls |
| `remotion-maps` | Map animation knowledge |
| `remotion-markup` | Content, animation, effects best practices |
| `remotion-multimedia` | Mediabunny integration (audio/video streams) |
| `remotion-render` | Export settings, codec, quality flags |
| `remotion-saas` | Building Remotion-based SaaS apps |
| `remotion-studio` | Studio preview, composition sidebar |
| `remotion-upgrade` | Version upgrades, migration notes |

## Usage in Niumination context

Only `remotion-create`, `remotion-markup`, and `remotion-render` are relevant for the Konten Kreator workflow. The rest are reference — load via `skill_view(name='remotion-project/remotion-<topic>')` if needed.

**Warning:** These are hub-installed skills (managed by `npx remotion skills add`). Do NOT edit their SKILL.md directly — edits will be overwritten on re-install. Custom adaptations go in `skills/content/remotion-video/`.
