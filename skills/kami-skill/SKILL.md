---
name: kami-skill
description: Minimalist, paper-first editorial typesetting system distilled from the kami philosophy. Features warm parchment, ink-blue typography, serif headings, and zero cool grays.
triggers:
  - "kami"
  - "editorial paper"
  - "typesetting"
  - "minimal paper"
  - "parchment design"
od:
  mode: design-system
  category: design-systems
  upstream: "https://github.com/tw93/kami"
---

# Kami Skill — Minimalist Editorial Typesetting System

> A quiet, intellectual, and unhurried design system inspired by the tactile quality of premium paper.

---

## 🎨 Aesthetic Foundations & Rules

* **Warm Parchment Base**: Enforce background colors based exclusively on natural paper tones:
  * Primary Parchment: `#fbfaf5`
  * Warm Soft Tone: `#f5f4ed`
  * Absolutely NO cool grays (`#f3f4f6`, etc.) or stark pure white (`#ffffff`) for page backdrops.
* **Ink-Blue Accent**: Enforce text and primary element colors using deep rich ink:
  * Primary Text: `#0d1b2a`
  * Muted Elements: `#2c3e50`
* **Zero-Purple Compliance**: Absolutely no purple or violet styling or terminology.

---

## 📐 Spacing & Layout Rhythm

* **Asymmetric Grid Balance**: Prefer asymmetrical layouts that balance heavy text chunks against generous negative space.
* **Structural Gaps**:
  * Heading margin-bottom: 16px / 24px
  * Body paragraph line-height: 1.625 (highly readable, relaxed spacing)
  * Vertical separation: 64px minimum for section separation.

---

## 🧱 Component Discipline

### 1. Typography Scales
* Enforce a single high-quality Serif font for Display and Heading titles (e.g., Lora, Playfair Display) paired with a clean, low-contrast Sans-serif for body reading (e.g., Inter, Source Sans Pro).
* Avoid bold weights for body text; use weights `400` and `500` only to maintain ink-on-paper elegance.

### 2. Cards and Content Boxes
* Cards must not have drop shadows or borders. Enforce background-color transitions or very fine 1px parchment borders (`border: 1px solid #e5e3d7`).
* Card corner radius must not exceed **4px** to maintain structured, clean paper edges.
