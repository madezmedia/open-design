# Plan: clinical-storyboard design kit

Checklist to implement the **clinical-storyboard** design template in the `open-design` repository.

## Action Checklist

- [ ] **Task 1: Scaffold Skill Metadata (`design-templates/clinical-storyboard/SKILL.md`)**
  - Write `SKILL.md` following standard Claude Code skill headers.
  - Define custom `od:` frontmatter: scenario (Clinical), platform (web-prototype), fidelity (high).
  - *Verification:* Confirm file exists and parses YAML frontmatter cleanly.

- [ ] **Task 2: Configure Properties & Variables (`design-templates/clinical-storyboard/template.json`)**
  - Define template.json properties: `deckTitle`, `storyId`, `narrative`, `panelIndex`, `totalPanels`, `coordinates`.
  - Add preset inputs matching our social stories templates.
  - *Verification:* Validate JSON syntax using local parser.

- [ ] **Task 3: Draft Tactile Swatch CSS (`design-templates/clinical-storyboard/assets/css/styles.css`)**
  - Set CSS variables: `--od-paper-bg: #FBFAF5`, `--od-ink-text: #0D1B2A`, `--od-signal-coral: #A54B40`, `--od-forest-green: #2D4A3E`.
  - Design editorial layout, solid 1px paper borders, and flat monospaced chip lists.
  - *Verification:* Scan file to ensure absolute compliance with the zero-purple rules.

- [ ] **Task 4: Program Anime.js v4 Spring Physics (`design-templates/clinical-storyboard/assets/js/springs.js`)**
  - Import tree-shakeable `animate` from `animejs`.
  - Wire hover elastic-scaling (`scale: 1.018`, `easeOutElastic`) and staggered intersection reveals.
  - *Verification:* Confirm ESM syntax matches Anime.js v4 requirements.

- [ ] **Task 5: Assemble Demonstration Spread (`design-templates/clinical-storyboard/example.html`)**
  - Create interactive storyboard maker page showing illustration slots, narrative fields, and customizable AAC card cues.
  - Link standard styles.css and springs.js.
  - *Verification:* Open in local browser to check Fitts' law target sizes (>= 44px).

- [ ] **Task 6: Validate Integration & Compile**
  - Run project-level checks to verify the new skill is auto-detected:
    ```bash
    pnpm guard
    pnpm typecheck
    ```
  - *Verification:* 100% clean passes without type or linter errors.
