---
name: clinical-storyboard
description: |
  A clinical storyboard template for safety social stories and Functional Communication Training (FCT) visual cards.
  Designed for neurodiversity-affirming lessons. Use when the brief mentions "social story", "safety storyboard",
  "behavioral deck", "visual cards", or "elopement prevention".
triggers:
  - "social story"
  - "safety storyboard"
  - "behavioral deck"
  - "visual cards"
  - "elopement prevention"
  - "canva storyboard"
od:
  mode: prototype
  platform: web-prototype
  scenario: education
  preview:
    type: html
    entry: example.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  example_prompt: "Create an 8-panel safety social storybook deck for staying with my group, using textured hand-drawn vector elements and warm paper backgrounds."
---

# Clinical Storyboard Skill

Produce a multi-spread customizable safety social storybook and clinical visual card deck.

## Workflow

1. Read DESIGN.md.
2. Layout:
   - Header: Monospaced telemetry tags, clinical deck index, coordinates stamp.
   - Core illustration: Large picture slot frame designed for dynamic Fal Recraft Vector illustration assets.
   - Narrative caption: A tactile paper caption block displaying behavior-analytic story text in italic editorial serifs.
   - Interactive Visual cards: Double-column visual replacement mands (e.g. "Request Space", "Emergency Call") with Fitts' Law target sizes (>= 44px).
3. Easing & Motion:
   - Program staggering entry reveals for story cards on scroll.
   - Apply elastic spring scales (scale: 1.018) on active item clicks and indicators.

## Output contract

```
<artifact identifier="clinical-storyboard-preview" type="text/html" title="Clinical Storyboard">
<!doctype html>...</artifact>
```
