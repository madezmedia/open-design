---
name: taste-skill
description: High-agency design taste system that enforces design restraint, visual density, and anti-slop principles for professional frontend interfaces.
triggers:
  - "design taste"
  - "visual taste"
  - "good taste"
  - "anti slop"
  - "visual density"
od:
  mode: design-system
  category: design-systems
  upstream: "https://github.com/Leonxlnx/taste-skill"
---

# Taste Skill — Aesthetic Restraint and Anti-Slop System

> A curated design framework to inject high-agency, professional aesthetic judgment into AI-generated interfaces.

---

## 🎨 Brand Philosophy & Aesthetic

* **Restraint is Luxury**: Design is defined by what you leave out, not what you pack in. Every element must earn its place on the screen.
* **Anti-Slop Directive**: Absolutely no generic AI-generated blobs, mesh gradients, floating neon bubbles, or rounded-everything card lists.
* **Atmosphere**: Professional, data-informed, highly polished. Warm paper base (`#faf9f5`), charcoal text (`#1a1a1a`), and forest green accents (`#2d4a3e`). Absolute compliance with the zero-purple/violet restriction.

---

## 📐 Foundations & Visual Density

| Foundation | Specification | Intent |
|---|---|---|
| **Whitespace** | Generous, breathy, mathematical padding (multiples of 8px). | Gives interfaces visual breathing room and high-end feel. |
| **Visual Density** | Tunable density scales (Comfortable, Standard, Compact). | Adapts to user workflows and prevents cognitive overload. |
| **Layout Variance** | Asymmetric columns, dramatic type scale ratios. | Breaks away from predictable left-to-right split grids. |

---

## 🧱 Component Rules & Spacing

### 1. Typography Scales
* **Display Scale**: 1.5 - 1.618 ratio for bold display titles.
* **Body Text**: 16px minimum on web, line height 1.5 - 1.6, line length limited to 45-75 characters.
* **Primary Fonts**: Premium sans-serif (Inter, Outfit) paired with high-character serif headings for luxury, or monospaced labels for technical depth.

### 2. Spacing Ratios
* Spacing must strictly follow an 8-point mathematical grid system:
  * Micro padding: 4px / 8px
  * Structural gap: 16px / 24px / 32px
  * Section layout margin: 48px / 64px / 80px

---

## 🏁 Quality Gates & Guidelines
* Verify color contrast ratios meet WCAG 2.2 AA standards (minimum 4.5:1 for standard text).
* Do not use float layouts; enforce Flexbox or CSS Grid exclusively.
* Test responsiveness across three distinct breakpoints: Mobile (320px-639px), Tablet (640px-1023px), and Desktop (1024px+).
