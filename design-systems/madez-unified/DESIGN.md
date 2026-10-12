# Madez Media Unified Design System (madez-unified)

> Category: Enterprise Dark Glassmorphism & Editorial Warm Parchment
> Luminous obsidian surfaces, translucent glass cards, electric blue interaction signals, and warm parchment editorial accents for modern AI product suites.

## 1. Visual Theme & Atmosphere

Luminous obsidian surfaces, translucent glass cards, electric blue interaction signals, and warm parchment editorial accents for modern AI product suites.

- **Visual style:** dark mode glassmorphism, warm parchment editorial, high-contrast HUD, sleek liquid obsidian
- **Color stance:** deep void black, dark charcoal surface, electric blue primary, cyber cyan accent, warm parchment editorial highlight
- **Design intent:** Unify visual identity across Madez Media agency properties, OpenDesign 0.7.0 studio canvas, Whop storefronts, and ACMI fleet telemetry.

## 2. Color

- **Primary:** `#1856FF` — Electric Blue (primary CTA & interaction signal).
- **Secondary:** `#00F0FF` — Cyber Cyan (fleet telemetry & active node status).
- **Accent Parchment:** `#F5EBE0` — Warm Parchment (editorial headings & key takeaways).
- **Success:** `#07CA6B` — Luminous Emerald Green (status active / shipped).
- **Warning:** `#E89558` — Amber Gold (blockers / pending review).
- **Danger:** `#EA2143` — Crimson Red (critical error / system down).
- **Base Void:** `#0B0C10` — Deep Void Black (page background).
- **Surface Glass:** `rgba(18, 20, 29, 0.70)` — Translucent Charcoal Glass.
- **Border Glass:** `rgba(255, 255, 255, 0.08)` — Frosted Glass Border.
- **Text Primary:** `#F8FAFC` — Crisp White Text.
- **Text Secondary:** `#94A3B8` — Slate Gray Subtext.
- **Text Muted:** `#64748B` — Muted Caption.

- Favor Primary (#1856FF) for main CTA buttons and active tab indicators.
- Use Surface Glass (`rgba(18, 20, 29, 0.70)`) with `backdrop-filter: blur(16px)` for floating control panels and cards.
- Use Accent Parchment (#F5EBE0) for pull quotes, badges, and warm editorial headlines.

## 3. Typography

- **Scale:** High-density, mobile-first responsive scale.
- **Families:** 
  - `display`: GT Sectra, Plus Jakarta Sans, Clash Display
  - `primary`: Inter, Söhne, system-ui
  - `mono`: JetBrains Mono, Fira Code
- **Weights:** 300, 400, 500, 600, 700
- Headings carry the editorial warmth of GT Sectra / Plus Jakarta Sans; body copy optimizes dark mode scanability with Inter.

## 4. Spacing & Grid

- **Spacing scale:** 4px baseline, 8px grid (4, 8, 12, 16, 24, 32, 48, 64px).
- Maintain consistent vertical rhythm across dark glass card panels.
- Align metrics and fleet status nodes to structured multi-column grids.

## 5. Layout & Composition

- Multi-panel dark glass HUD layout with subtle 1px frosted glass borders.
- Clear structural hierarchy: Header Badge → Warm Parchment Headline → Dark Glass Body → Primary Electric Blue Action.
- Whitespace and backdrop-blur separation before solid divider lines.

## 6. Components

- **Buttons:** Primary uses `#1856FF` with subtle hover glow (`box-shadow: 0 0 20px rgba(24, 86, 255, 0.4)`). Secondary uses translucent dark glass.
- **Inputs:** Translucent void backgrounds (`#0B0C10`), 1px frosted border, electric blue focus ring.
- **Cards & Modals:** Translucent charcoal surface, `backdrop-filter: blur(16px)`, `1px solid rgba(255, 255, 255, 0.08)`.
- **Badges:** Compact monospace pills with neon status dots (`#07CA6B` active, `#00F0FF` node, `#F5EBE0` editorial).

## 7. Motion & Interaction

- Subtle 150-250ms cubic-bezier transitions (`cubic-bezier(0.16, 1, 0.3, 1)`).
- Micro-hover elevation on dark glass cards (`transform: translateY(-2px)`).
- Glowing electric blue pulse animation on active ACMI telemetry nodes.

## 8. Voice & Brand

- **Tone:** Technical, authoritative, editorial, high-agency, concise.
- **Microcopy:** Action-oriented, literal, clear, zero filler or generic placeholders.

## 9. Anti-patterns

- Do not use plain bright white backgrounds or harsh unstyled gray cards.
- Do not use purple/violet gradients (enforce Purple Ban rule).
- Do not drop contrast below WCAG AA on dark glass surfaces.
- Do not mix generic template layouts with high-density ACMI telemetry grids.
