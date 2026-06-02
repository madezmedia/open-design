# Open Design Spec: clinical-storyboard Kit
Date: 2026-06-02  
Author: Antigravity AI Coding Assistant  
Co-Authored-By: aba-bcba-expert <sheveenbrown@gmail.com>  
Status: PROPOSED (Awaiting User Review)

---

## 1. Goal & Context

The goal is to implement a new **clinical-storyboard** design kit in Open Design (`design-templates/clinical-storyboard/`). This template allows therapists, special education teachers, and caregivers to build, customize, and print safety-focused social stories and Functional Communication Training (FCT) visual cards.

The visual assets are dynamically generated using the **Fal Recraft Vector** model, utilizing the user-approved **Organic Hand-drawn (High-Personality)** aesthetic, and organized into a **Modular Folder Hierarchy** for clean developer-parent customization loops.

---

## 2. Design System Tokens (Kami Editorial Swatch)

The template strictly adheres to the visual restraint and zero-purple guidelines outlined in FBL-OS standards:
- **Surface Backdrop:** Natural warm parchment paper (`#FBFAF5` / `#FAF9F5`)
- **Main Text / Borders:** Deep ink-blue / dark navy charcoal (`#0D1B2A` / `#1A1A1A`)
- **Accent Signals:** Warm signal-coral (`#A54B40`) and clinical forest green (`#2D4A3E`)
- **Typography pairing:** Montserrat display sans-serif (telemetry tags, labels) paired with Raleway / Source Serif (editorial headings and narrative text)
- **Corner Radii:** Strictly restricted to crisp, paper-like borders (`rounded-[4px]` or `rounded-[2px]`)

---

## 3. Filesystem Architecture (Modular Template Tree)

The kit is structured in a clean, multi-spread directory layout to allow separate validation and editing:

```
design-templates/clinical-storyboard/
├── SKILL.md                 # Open Design skill definition
├── template.json            # Template metadata, variables, and presets
├── example.html             # Default interactive clinical demonstration page
└── assets/
    ├── css/
    │   └── styles.css       # Tactile editorial design system CSS tokens
    └── js/
        └── springs.js       # Anime.js v4 elastic spring-physics handlers
```

### Template variables (`template.json`):
```json
{
  "name": "clinical-storyboard",
  "fidelity": "high",
  "platform": "web-prototype",
  "variables": {
    "deckTitle": { "type": "string", "default": "Staying With My Group" },
    "storyId": { "type": "string", "default": "s1" },
    "narrative": { "type": "string", "default": "I stay with my group so we can have fun together." },
    "panelIndex": { "type": "number", "default": 1 },
    "totalPanels": { "type": "number", "default": 8 },
    "coordinates": { "type": "string", "default": "42.10 // -71.02" }
  }
}
```

---

## 4. Dynamic Fal Recraft Prompting Engine

The Open Design daemon handles dynamic illustration generation via the Fal Recraft Vector API.
- **Locked Visual Tokens (High-Personality Organic Hand-drawn):**  
  Every image call dynamically appends the prefix:  
  `"flat vector graphic, textured pencil-feel strokes, warm ivory background #FAF9F5, friendly cartoon child and caregiver, highly expressive positive friendly facial features, soft pencil-shading highlights, simple clean outlines, zero purple, high-taste professional illustration"`
- **LLM Translator Pipeline:**  
  The agent translates raw user text (e.g. *"I stop at the curb and wait for my grown-up"*) into an explicit descriptive scene (e.g. *"a little child standing safely at the edge of a curb, looking up at a smiling caregiver who holds a green stop sign"*) before executing the Fal API call.

---

## 5. Verification Plan

### Automated Checks
- **Zero-Purple Audit:**  
  Verify no hex codes matching violet/purple hues are introduced in `styles.css`.
- **Contrast Check:**  
  Ensure all copy elements maintain WCAG AA compliance (minimum `4.5:1` contrast ratio over warm parchment `#FAF9F5`).
- **TypeScript & Build passes:**  
  Validate folder imports through open-design checkouts:
  ```bash
  pnpm --filter @open-design/web typecheck
  pnpm --filter @open-design/web build
  ```

### Manual Acceptance Criteria
- Verify that clicking any storyboard element triggers the spring-physics animation fluidly at 60fps.
- Verify vector illustrations are rendered inside tactile paper borders with sharp 4px corners.
