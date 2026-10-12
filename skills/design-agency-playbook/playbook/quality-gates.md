# Quality Gates

> Part of the Design Agency Playbook — defines per-stage quality gates that must be satisfied before work items advance.

## Overview

Quality gates are checklists that each receiving agent verifies before accepting a handoff. They ensure that work meets minimum quality standards at every stage of the pipeline, preventing defects from cascading downstream.

## How Quality Gates Work

1. When a handoff is received, the receiving agent runs the quality gate checklist for the *sending* stage.
2. If all items pass, the agent acknowledges the handoff and begins their work.
3. If any item fails, the agent logs a `review-fail` or `handback` event with the specific failures.
4. The sending agent must address failures and resubmit.

---

## Stage 1: Research Quality Gate

> Checked by: `design-ux-architect` before accepting handoff from `design-ux-researcher`

### Gate Checklist

#### User Research
- [ ] Research methodology is documented and appropriate for the design challenge
- [ ] Minimum 5 user touchpoints analyzed (interviews, surveys, analytics)
- [ ] Research findings are backed by data, not assumptions
- [ ] User pain points are clearly identified and prioritized

#### Personas
- [ ] 1-3 primary user personas created
- [ ] Each persona has: name, role, goals, pain points, context
- [ ] Personas are based on research data (not stereotypes)
- [ ] Personas include accessibility considerations

#### Journey Maps
- [ ] Current-state journey maps created for key user flows
- [ ] Pain points and opportunities identified on each journey
- [ ] Emotional journey mapped alongside functional journey
- [ ] Key touchpoints highlighted

#### Competitive Analysis
- [ ] Minimum 3 competitors analyzed
- [ ] Competitive strengths and weaknesses documented
- [ ] Differentiation opportunities identified

#### Heuristic Evaluation
- [ ] Standard heuristics used (Nielsen's 10 or equivalent)
- [ ] Each heuristic scored with evidence
- [ ] Critical and major issues prioritized

#### Synthesis
- [ ] Research findings synthesized into actionable recommendations
- [ ] Recommendations directly linked to research data
- [ ] "How might we" questions or problem statements framed

### Failure Domains

| Domain | Impact | Escalate? |
|--------|--------|-----------|
| No research data (assumptions only) | High | Yes — block pipeline |
| Missing personas | High | Yes — block pipeline |
| Incomplete journey maps | Medium | No — conditional pass with request for supplement |
| Weak competitive analysis | Low | No — note for next iteration |

---

## Stage 2: Architecture Quality Gate

> Checked by: `design-ui-designer` before accepting handoff from `design-ux-architect`

### Gate Checklist

#### CSS Architecture
- [ ] Methodology chosen and documented (BEM, CUBE, utility-first, etc.)
- [ ] Naming convention defined
- [ ] File/folder structure defined
- [ ] CSS specificity strategy documented
- [ ] CSS custom properties (variables) plan in place

#### Design Tokens
- [ ] Color palette defined (primary, secondary, neutral, semantic)
- [ ] Typography scale defined (typefaces, sizes, weights, line heights)
- [ ] Spacing scale defined (unit system, spacing tokens)
- [ ] Breakpoint definitions for responsive design
- [ ] Border radius, shadow, and other effect tokens defined
- [ ] Animation timing/easing tokens defined (minimal)

#### Component Hierarchy
- [ ] Component tree diagram created
- [ ] Atomic design level or equivalent documented
- [ ] Component responsibility and boundaries defined
- [ ] Shared vs. page-specific components identified
- [ ] State variants accounted for (loading, empty, error, edge cases)

#### Responsive Layout
- [ ] Layout strategy documented (mobile-first, desktop-first)
- [ ] Grid system defined (columns, gutters, margins)
- [ ] Layout patterns cataloged (single, split, grid, etc.)
- [ ] Breakpoint behavior documented for each layout pattern

#### Design System
- [ ] Style guide foundation includes usage guidelines
- [ ] Token documentation includes usage examples
- [ ] Accessibility foundations included (focus, color contrast guidance)

### Failure Domains

| Domain | Impact | Escalate? |
|--------|--------|-----------|
| Missing design tokens | High | Yes — block pipeline |
| No component hierarchy | High | Yes — block pipeline |
| Undefined CSS methodology | Medium | No — request supplement |
| Partial token coverage | Medium | No — conditional pass |
| Missing responsive strategy | Medium | No — request supplement |

---

## Stage 3: Design Quality Gate

> Checked by: All 3 Review agents (`design-brand-guardian`, `design-visual-storyteller`, `design-inclusive-visuals-specialist`)

### Gate Checklist

#### Visual Execution
- [ ] All key screens/states designed
- [ ] Designs match the architecture spec
- [ ] Design tokens applied consistently throughout
- [ ] Responsive variants designed for target breakpoints
- [ ] Typography hierarchy clear and consistent
- [ ] Spacing and alignment follow the defined scale
- [ ] Color usage follows token definitions

#### Component Library
- [ ] All reusable components identified and built
- [ ] Component variants defined (sizes, states, themes)
- [ ] Components match the architecture component hierarchy
- [ ] Library organized and documented (naming, descriptions)

#### Prototype
- [ ] Key user flows prototyped
- [ ] Prototype reflects the intended user journey
- [ ] Navigation and transitions included in prototype

#### Platform Conventions
- [ ] Platform-specific conventions followed (iOS, Android, Web)
- [ ] Platform-appropriate components used
- [ ] Platform-appropriate gestures/interactions designed

### Failure Domains

| Domain | Impact | Escalate? |
|--------|--------|-----------|
| Missing key screens | High | Yes — block pipeline |
| Tokens not applied | High | Yes — block pipeline |
| Inconsistent spacing/alignment | Medium | No — return for polish |
| Missing responsive variants | Medium | No — return for supplement |
| Prototype incomplete | Low | No — note for next iteration |

---

## Stage 4: Brand Guardian Quality Gate

> Checked by: Orchestrator (after brand review, before advancing)

### Gate Checklist

#### Brand Colors
- [ ] All colors used are from the approved brand palette
- [ ] Accent colors used correctly (not for primary actions)
- [ ] Color semantics match brand guidance (error, success, warning)
- [ ] No brand color orphans (colors used without brand context)

#### Typography
- [ ] Typefaces used match brand type scale
- [ ] Hierarchy follows brand type scale
- [ ] Font weights and styles follow brand guidance
- [ ] Line heights and letter-spacing follow brand

#### Logo and Marks
- [ ] Logo usage follows brand guidelines (clear space, sizing)
- [ ] Correct logo variant used (full, icon, horizontal/vertical)
- [ ] Logo placement matches brand guidance
- [ ] No logo distortion or modification

#### Voice and Tone
- [ ] Copy tone matches brand voice
- [ ] Terminology consistent with brand glossary
- [ ] Messaging aligns with brand positioning

#### Visual Identity
- [ ] Photography style matches brand direction
- [ ] Illustration style matches brand direction
- [ ] Iconography style matches brand system
- [ ] Overall visual language is cohesive with brand

### Failure Domains

| Domain | Impact | Escalate? |
|--------|--------|-----------|
| Brand color misuse | High | Yes — block pipeline |
| Logo misuse | High | Yes — block pipeline |
| Typography inconsistency | Medium | No — return for fix |
| Tone inconsistency | Medium | No — return for fix |
| Minor style drift | Low | No — note for next iteration |

---

## Stage 5: Storyteller Quality Gate

> Checked by: Orchestrator (after storytelling review, before advancing)

### Gate Checklist

#### Information Hierarchy
- [ ] Primary information is visually prominent
- [ ] Secondary and tertiary information is clearly subordinate
- [ ] Content groupings are logical and scannable
- [ ] Call-to-actions are positioned for visual flow

#### Narrative Flow
- [ ] Visual sequence guides the user logically through the experience
- [ ] Each screen/scene builds on the previous one
- [ ] Story arc supports the user's goal
- [ ] No narrative dead ends or confusing transitions

#### Data Visualization
- [ ] Charts and graphs are clear and accurate
- [ ] Data-ink ratio is optimized (minimal chart junk)
- [ ] Labels and legends are readable
- [ ] Color in data viz is accessible (pattern fill where needed)

#### Illustrations
- [ ] Illustration style is consistent throughout
- [ ] Illustrations communicate the intended message
- [ ] Illustrations complement (not compete with) content
- [ ] Are illustrations meaningful or decorative? (prefer meaningful)

### Failure Domains

| Domain | Impact | Escalate? |
|--------|--------|-----------|
| Narrative flow broken | High | Yes — block pipeline |
| Information hierarchy wrong | High | Yes — block pipeline |
| Confusing data viz | Medium | No — return for fix |
| Inconsistent illustration | Low | No — note for polish |

---

## Stage 6: Accessibility Quality Gate

> Checked by: Orchestrator (after accessibility review, before advancing)

### Gate Checklist

#### WCAG 2.1 Compliance (Level AA minimum)
- [ ] 1.1.1 Non-text Content (all images have alt text)
- [ ] 1.4.3 Contrast (Minimum) — 4.5:1 for normal text, 3:1 for large text
- [ ] 1.4.11 Non-text Contrast — UI components meet 3:1
- [ ] 2.1.1 Keyboard — all functionality available via keyboard
- [ ] 2.4.3 Focus Order — focusable elements in logical sequence
- [ ] 2.4.7 Focus Visible — visible focus indicator on all interactive elements
- [ ] 2.4.6 Headings and Labels — descriptive headings and labels
- [ ] 3.3.2 Labels or Instructions — labels provided for all inputs

#### Color and Contrast
- [ ] Color contrast validated with tools (WebAIM, axe, Lighthouse)
- [ ] No color-only information conveyance
- [ ] Focus states meet contrast requirements
- [ ] Error states meet contrast requirements

#### Keyboard Accessibility
- [ ] Tab order matches visual order
- [ ] All interactive elements are keyboard reachable
- [ ] No keyboard traps
- [ ] Skip navigation links present

#### Screen Reader
- [ ] ARIA landmarks used correctly
- [ ] Roles and properties properly assigned
- [ ] Dynamic content announced (aria-live regions)
- [ ] Forms have proper labels and error announcements

#### Inclusive Design
- [ ] Content avoid ableist language and imagery
- [ ] Diverse representation in illustrations and photography
- [ ] Forms respect cognitive accessibility (clear instructions, forgiving validation)
- [ ] Reduced motion alternatives provided for animations

### Failure Domains

| Domain | Impact | Escalate? |
|--------|--------|-----------|
| Color contrast fails | High | Yes — block until fixed |
| Keyboard trap | High | Yes — block pipeline |
| Missing alt text on key images | High | Yes — block until fixed |
| ARIA misuse | Medium | No — return for fix |
| Minor contrast issues | Medium | No — return for fix |
| Representation concerns | Medium | No — return for fix |

---

## Stage 7: Delight Quality Gate

> Checked by: `design-image-prompt-engineer` before accepting handoff from `design-whimsy-injector`

### Gate Checklist

#### Micro-interactions
- [ ] Interactions enhance the experience (not distract)
- [ ] Hover states provide meaningful feedback
- [ ] Transitions are smooth and purposeful
- [ ] Loading states are engaging (not just spinners)
- [ ] Error states include helpful animations/feedback

#### Animation
- [ ] Animation durations are consistent (base unit established)
- [ ] Easing curves are cohesive across the experience
- [ ] Animations respect `prefers-reduced-motion`
- [ ] No animation causes motion sickness or discomfort
- [ ] Sequential animations have proper choreography

#### Delight Elements
- [ ] Each delight element serves a purpose (functional or emotional)
- [ ] Delight does not impede task completion
- [ ] Celebratory moments are appropriate for context
- [ ] Easter eggs are discoverable but not distracting

#### Motion Design Language
- [ ] Motion principles documented (not just ad-hoc)
- [ ] Shared transitions use consistent timing/easing
- [ ] Motion supports the brand personality
- [ ] Motion hierarchy matches visual hierarchy

### Failure Domains

| Domain | Impact | Escalate? |
|--------|--------|-----------|
| Animation causes motion issues | High | Yes — block pipeline |
| Delight impedes functionality | High | Yes — block pipeline |
| No reduced-motion alternative | Medium | No — return for fix |
| Inconsistent timing/easing | Low | No — note for polish |
| Over-designed elements | Low | No — note for refinement |

---

## Stage 8: Assets Quality Gate

> Checked by: Orchestrator (before marking Done)

### Gate Checklist

#### Image Assets
- [ ] All required images produced per design spec
- [ ] Image resolutions suitable for target display densities (1x, 2x, 3x)
- [ ] Images optimized for web delivery (size, format)
- [ ] Next-gen formats provided (WebP, AVIF) with fallbacks
- [ ] Image quality acceptable (no artifacts, correct colors)

#### Icons
- [ ] Icons consistent with design system style
- [ ] Icon set covers all required use cases
- [ ] Icons available in required sizes
- [ ] SVG icons optimized (clean paths, no unnecessary markup)
- [ ] Icons have proper accessible labels

#### Asset Organization
- [ ] Asset naming convention followed consistently
- [ ] Assets organized in logical directory structure
- [ ] Asset inventory (manifest) created
- [ ] Copyright/licensing documented for AI-generated assets

#### Formats
- [ ] Each asset in appropriate format (SVG, PNG, JPEG, WebP)
- [ ] Format chosen balances quality vs. file size
- [ ] No unnecessary asset bloat (remove unused variants)

### Failure Domains

| Domain | Impact | Escalate? |
|--------|--------|-----------|
| Missing critical asset | High | Yes — block pipeline |
| Assets not optimized | Medium | No — return for optimization |
| Inconsistent icon style | Medium | No — return for fix |
| Poor naming convention | Low | No — note for next time |
| Missing alt text | Medium | No — return for supplement |

---

## Final Validation Gate (Done)

> Checked by: Orchestrator before marking work item complete

### Gate Checklist

#### Completeness
- [ ] All 8 pipeline stages completed
- [ ] All handoff events logged in ACMI
- [ ] All review events logged (review-pass x 3)
- [ ] All quality gates passed
- [ ] All deliverables produced per stage

#### ACMI Recording
- [ ] Work item signals updated to "completed"
- [ ] Final milestone-shipped event logged
- [ ] Work item timeline shows complete handoff chain
- [ ] All correlationIds properly chained

#### Delivery
- [ ] Deliverable package assembled
- [ ] Delivery sent to stakeholder
- [ ] Stakeholder acknowledged receipt

---

## Gate Failure Escalation Procedure

1. **First failure** — Work returned to originating stage. Document failures in `review-fail` event.
2. **Second failure** — Work returned again. Document failures. Add note to coordinator thread.
3. **Third failure** — Escalation triggered. Orchestrator creates escalation event and notifies stakeholder.

### Escalation Event

```typescript
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "system:orchestrator",
  kind: "coord-note",
  correlationId: "<workItemId>Escalation-<epochMs>",
  summary: "[coord-note @stakeholder] <work-item-title> — escalated after 3 rework cycles at <stage-name> stage"
)
```

### Re-entry After Escalation

After escalation, a human stakeholder reviews the situation and decides:
1. **Override** — Accept the work despite gate failures (log as `scope-decision`)
2. **Rewrite** — Restart the stage with fresh approach (reset work item back to appropriate stage)
3. **Abort** — Cancel the work item (log as `work-completed` with status "cancelled")
