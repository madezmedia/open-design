# Pipeline Flow

> Part of the Design Agency Playbook — details the full kanban pipeline workflow.

## Overview

The Design Agency Pipeline is a sequential kanban system with 8 stages. Work items flow from Backlog through specialized agents to completion. Each stage is owned by a dedicated agent with specific skills and quality criteria.

```
Backlog → Research → Architecture → Design → Review → Delight → Assets → Done
```

## Stage 1: Backlog

**Owner:** System / Orchestrator

### Description
New design requests enter the pipeline here. Backlog is where design briefs are filed, prioritized, and prepared for the design team.

### Activities
- Receive design requests from stakeholders
- Document design brief with requirements, scope, and constraints
- Assign priority (low, medium, high, critical)
- Tag with relevant categories (UI, brand, marketing, product)
- Correlate with existing work to prevent duplication

### ACMI Operations
```typescript
// Create work item in backlog
acmi_work_create(
  id: "<unique-id>",
  profile: JSON.stringify({
    title: "<design-challenge-title>",
    description: "<full-design-brief>",
    priority: "high|medium|low",
    requester: "<stakeholder>",
    stage: "backlog",
    created_at: "<iso-timestamp>"
  })
)

// Log creation event
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "system:orchestrator",
  kind: "work-created",
  correlationId: "<workItemId>Created-<epochMs>",
  summary: "[work-created @design-team] New design request: <title>"
)
```

### Entry Criteria
- Design brief exists with clear requirements
- Stakeholder identified
- Priority assigned

### Exit Criteria
- Work item created in ACMI
- Correlation chain established
- Ready for assignment to Research

---

## Stage 2: Research

**Owner:** 🔍 design-ux-researcher

### Description
The Research stage grounds the design in real user needs. The UX researcher conducts user research, analyzes competitors, creates personas, maps user journeys, and evaluates existing designs against heuristics.

### Activities
- Review design brief and requirements
- Conduct user research (interviews, surveys, analytics review)
- Perform competitive analysis
- Create or update user personas
- Map user journeys and flows
- Conduct heuristic evaluation of existing solutions
- Synthesize findings into actionable recommendations
- Document research artifacts

### ACMI Operations
```typescript
// Agent starts work
acmi_signal(
  namespace: "agent",
  id: "design-ux-researcher",
  signals: JSON.stringify({
    status: "working",
    current_work_item: "<work-item-id>",
    current_stage: "research",
    started_at: "<iso-timestamp>"
  })
)

// Log research milestone
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:design-ux-researcher",
  kind: "milestone-shipped",
  correlationId: "uxResearcherResearchComplete-<epochMs>",
  summary: "[milestone-shipped @design-ux-architect] Research complete for <work-item-title>"
)

// Handoff to Architecture
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:design-ux-researcher",
  kind: "handoff-complete",
  correlationId: "uxResearcherHandoffToArchitect-<epochMs>",
  summary: "[handoff-complete @design-ux-architect] <work-item-title> — research artifacts ready"
)

// Signal complete
acmi_signal(
  namespace: "agent",
  id: "design-ux-researcher",
  signals: JSON.stringify({
    status: "idle",
    current_work_item: null,
    current_stage: null,
    last_completed: "<work-item-id>"
  })
)
```

### Deliverables
- Research report (synthesized findings)
- User personas (1-3 primary personas)
- Journey maps (current state)
- Competitive analysis matrix
- Heuristic evaluation report
- UX recommendations document

### Entry Criteria
- Work item assigned with clear brief
- Scope and constraints documented

### Exit Criteria
- Research deliverables complete
- Research artifacts attached to work item
- Handoff event logged to Architecture

---

## Stage 3: Architecture

**Owner:** 🏗️ design-ux-architect

### Description
The Architecture stage establishes the structural foundation. The UX architect defines the CSS architecture, design tokens, component hierarchy, responsive layout strategy, and design system foundations that will guide the visual design.

### Activities
- Review research report and user flows
- Define CSS architecture methodology (BEM, CUBE, utility-first, etc.)
- Establish design tokens (colors, typography, spacing, breakpoints)
- Map component hierarchy and relationships
- Plan responsive layout strategy
- Document grid system
- Define layout patterns and templates
- Create style guide foundation

### ACMI Operations
```typescript
// Agent starts work
acmi_signal(
  namespace: "agent",
  id: "design-ux-architect",
  signals: JSON.stringify({
    status: "working",
    current_work_item: "<work-item-id>",
    current_stage: "architecture",
    started_at: "<iso-timestamp>"
  })
)

// Handoff to Design
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:design-ux-architect",
  kind: "handoff-complete",
  correlationId: "uxArchitectHandoffToDesigner-<epochMs>",
  summary: "[handoff-complete @design-ui-designer] <work-item-title> — architecture spec ready"
)
```

### Deliverables
- CSS architecture specification
- Design token definition (JSON or CSS custom properties)
- Component hierarchy diagram
- Responsive layout strategy
- Grid system specification
- Layout pattern library
- Style guide foundation

### Entry Criteria
- Research report available
- User needs and flows documented

### Exit Criteria
- Architecture spec complete and documented
- Design tokens defined
- Component hierarchy mapped
- Handoff event logged to Design

---

## Stage 4: Design

**Owner:** 🎨 design-ui-designer

### Description
The Design stage is where visual design comes to life. The UI designer creates pixel-perfect visual designs, builds component libraries, and produces interactive prototypes informed by the architecture foundation and research insights.

### Activities
- Review architecture spec and design tokens
- Create wireframes and mockups
- Apply design tokens to visual designs
- Build component library
- Design responsive variants
- Create interactive prototype
- Document design decisions
- Prepare design handoff package

### ACMI Operations
```typescript
// Agent starts work
acmi_signal(
  namespace: "agent",
  id: "design-ui-designer",
  signals: JSON.stringify({
    status: "working",
    current_work_item: "<work-item-id>",
    current_stage: "design",
    started_at: "<iso-timestamp>"
  })
)

// Handoff to Review (all 3 reviewers)
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:design-ui-designer",
  kind: "handoff-complete",
  correlationId: "uiDesignerHandoffToReview-<epochMs>",
  summary: "[handoff-complete @design-brand-guardian,design-visual-storyteller,design-inclusive-visuals-specialist] <work-item-title> — designs ready for review"
)
```

### Deliverables
- Wireframes (low to high fidelity)
- Visual mockups (all key screens/states)
- Component library (with variants)
- Interactive prototype
- Design decisions document
- Responsive design variants

### Entry Criteria
- Architecture spec available
- Design tokens defined
- Component hierarchy mapped

### Exit Criteria
- Visual designs match architecture spec
- Component library populated
- Prototype functional
- Handoff event logged to Review

---

## Stage 5: Review (Parallel)

**Owners:** 🛡️ design-brand-guardian, 📖 design-visual-storyteller, ♿ design-inclusive-visuals-specialist

### Description
The Review stage runs three parallel review processes. Each reviewer evaluates the design from their specialty perspective. All three must pass before the work can advance.

### Activities

#### Brand Guardian
- Audit brand guideline compliance
- Verify color usage against brand palette
- Check typography against brand type scale
- Validate logo and brand mark usage
- Review voice and tone consistency
- Assess overall brand identity cohesion

#### Visual Storyteller
- Evaluate information hierarchy
- Review narrative flow and structure
- Assess visual communication effectiveness
- Check data visualization clarity
- Review illustration and graphic consistency
- Validate storyboard coherence

#### Inclusive Visuals Specialist
- Run WCAG 2.1 AA compliance check
- Verify color contrast ratios
- Check keyboard accessibility
- Review focus states and navigation
- Validate screen reader compatibility
- Assess inclusive design practices
- Review alt text and labeling

### ACMI Operations
```typescript
// Each reviewer acknowledges
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:<reviewer-id>",
  kind: "handoff-ack",
  parentCorrelationId: "<uiDesignerHandoffCorrelationId>",
  correlationId: "<reviewerId>Ack-<epochMs>",
  summary: "[handoff-ack] <reviewer> reviewing <work-item-title>"
)

// Each reviewer passes
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:<reviewer-id>",
  kind: "review-pass",
  correlationId: "<reviewerId>ReviewPass-<epochMs>",
  summary: "[review-pass] <reviewer> approved <work-item-title>"
)

// On failure
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:<reviewer-id>",
  kind: "review-fail",
  correlationId: "<reviewerId>ReviewFail-<epochMs>",
  summary: "[review-fail] <reviewer> flagged issues in <work-item-title>: <issues>"
)
```

### Deliverables
- Brand compliance report (Brand Guardian)
- Narrative review report (Storyteller)
- Accessibility audit report (Accessibility)
- Consolidated review report

### Entry Criteria
- Visual designs complete
- Component library populated
- Prototype available

### Exit Criteria
- All 3 reviewers pass
- Review reports attached to work item
- Consolidated review summary produced
- Handoff event logged to Delight

---

## Stage 6: Delight

**Owner:** ✨ design-whimsy-injector

### Description
The Delight stage adds the polish and personality that makes the design memorable. The whimsy injector designs micro-interactions, animations, and delightful touches that enhance the user experience.

### Activities
- Review approved design
- Identify opportunities for delight
- Design micro-interactions (hover states, transitions, feedback)
- Plan animation sequences
- Define motion design language
- Create animation specs (timing, easing, choreography)
- Document reduced-motion alternatives
- Design celebratory moments (confetti, success states, Easter eggs)

### ACMI Operations
```typescript
acmi_signal(
  namespace: "agent",
  id: "design-whimsy-injector",
  signals: JSON.stringify({
    status: "working",
    current_work_item: "<work-item-id>",
    current_stage: "delight",
    started_at: "<iso-timestamp>"
  })
)

// Handoff to Assets
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:design-whimsy-injector",
  kind: "handoff-complete",
  correlationId: "whimsyInjectorHandoffToAssets-<epochMs>",
  summary: "[handoff-complete @design-image-prompt-engineer] <work-item-title> — delight elements ready"
)
```

### Deliverables
- Micro-interaction specifications
- Animation sequence definitions
- Motion design language document
- Timing and easing charts
- Reduced-motion alternatives
- Delight element inventory

### Entry Criteria
- Design passes all 3 review gates
- Consolidated review report available

### Exit Criteria
- Delight elements designed and documented
- Animation specs complete
- Handoff event logged to Assets

---

## Stage 7: Assets

**Owner:** 🖼️ design-image-prompt-engineer

### Description
The Assets stage produces all visual assets needed for the design. The image prompt engineer crafts AI generation prompts, creates custom illustrations, generates icons, and produces optimized visual assets.

### Activities
- Review final design with delight elements
- Identify required visual assets
- Craft AI image generation prompts
- Generate custom illustrations and icons
- Create image variants (light/dark mode, responsive sizes)
- Optimize images for web delivery
- Produce asset inventory and naming convention
- Version and organize asset files

### ACMI Operations
```typescript
acmi_signal(
  namespace: "agent",
  id: "design-image-prompt-engineer",
  signals: JSON.stringify({
    status: "working",
    current_work_item: "<work-item-id>",
    current_stage: "assets",
    started_at: "<iso-timestamp>"
  })
)

// Handoff to Done
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:design-image-prompt-engineer",
  kind: "handoff-complete",
  correlationId: "imageEngineerHandoffToDone-<epochMs>",
  summary: "[handoff-complete @orchestrator] <work-item-title> — all assets delivered"
)
```

### Deliverables
- AI-generated illustrations
- Custom icons and icon sets
- Image assets (hero images, backgrounds, patterns)
- Responsive image variants
- Asset optimization report
- Asset inventory (names, formats, sizes, paths)

### Entry Criteria
- Design finalized with delight elements
- Animation specs complete

### Exit Criteria
- All visual assets generated and optimized
- Asset inventory populated
- Handoff event logged to Done

---

## Stage 8: Done

**Owner:** System / Orchestrator

### Description
The final stage validates everything, packages deliverables, and closes the work item. This is the terminal state — no handoff beyond this point.

### Activities
- Validate final deliverable package
- Run final quality gate checks
- Package all artifacts
- Deliver to stakeholder
- Close work item
- Log final milestone
- Archive deliverables

### ACMI Operations
```typescript
// Final milestone
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "system:orchestrator",
  kind: "milestone-shipped",
  correlationId: "<workItemId>Completed-<epochMs>",
  summary: "[milestone-shipped @stakeholder] Pipeline complete for <work-item-title>"
)

// Mark work item complete
acmi_work_signal(
  id: "<work-item-id>",
  signals: JSON.stringify({
    status: "completed",
    completed_at: "<iso-timestamp>",
    completed_by: "design-agency-pipeline"
  })
)

// Close event
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "system:orchestrator",
  kind: "work-completed",
  correlationId: "<workItemId>Done-<epochMs>",
  summary: "[work-completed] <work-item-title> delivered to <stakeholder>"
)
```

### Deliverables
- Complete design deliverable package
- Final quality gate report
- Delivery confirmation

### Entry Criteria
- All assets delivered
- Asset inventory verified

### Exit Criteria
- Work item marked complete
- Final milestone logged
- Deliverable delivered to stakeholder
