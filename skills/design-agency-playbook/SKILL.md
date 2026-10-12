---
name: design-agency-playbook
description: | 
  Master playbook for the Design Agency Pipeline — an 8-agent design team that processes design work through a kanban pipeline: Backlog -> Research -> Architecture -> Design -> Review -> Delight -> Assets -> Done. Integrates with ACMI for persistent agent coordination and the Open Design daemon for spawning agents. Each agent has a specialized role and handoff protocol.
triggers:
  - "design agency"
  - "design team"
  - "design pipeline"
  - "design agency playbook"
  - "design-agency-pipeline"
  - "open design team"
  - "8 agents"
od:
  mode: utility
  category: design-systems
  project: design-agency-pipeline
version: 1.0.0
tags:
  - design
  - pipeline
  - agents
  - kanban
  - acmi
  - team
  - playbook
---

# Design Agency Playbook

> Version 1.0.0 | Open Design Project: `design-agency-pipeline`

The Design Agency Playbook orchestrates an 8-agent design team that processes work through a kanban pipeline. Each agent is a specialized designer registered in ACMI with persistent profile, signals, and timeline — enabling cross-session coordination and full traceability of every design decision.

## Table of Contents

1. [Team Overview](#team-overview)
2. [Pipeline Workflow](#pipeline-workflow)
3. [Agent Handoff Protocol](#agent-handoff-protocol)
4. [Quality Gates](#quality-gates)
5. [ACMI Coordination](#acmi-coordination)
6. [Open Design Daemon Integration](#open-design-daemon-integration)
7. [Project Reference](#project-reference)

---

## Team Overview

The Design Agency consists of 8 specialized agents, each owning a stage in the pipeline. Every agent has a canonical ACMI identity under `namespace:agent` and follows the same profile/signals/timeline contract.

| # | Agent | Role | Avatar | Stage |
|---|-------|------|--------|-------|
| 1 | `design-ux-researcher` | User Research | 🔍 | Research |
| 2 | `design-ux-architect` | CSS/Systems Foundation | 🏗️ | Architecture |
| 3 | `design-ui-designer` | Visual Design, Components | 🎨 | Design |
| 4 | `design-brand-guardian` | Brand Consistency | 🛡️ | Review |
| 5 | `design-visual-storyteller` | Narrative Visuals | 📖 | Review |
| 6 | `design-whimsy-injector` | Delight/Polish | ✨ | Delight |
| 7 | `design-inclusive-visuals-specialist` | Accessibility | ♿ | Review |
| 8 | `design-image-prompt-engineer` | AI Image Assets | 🖼️ | Assets |

### Agent Personas

Each agent has a distinct persona profile in ACMI:

- **🏗️ design-ux-architect** — The structural backbone. Builds scalable CSS architecture and design system foundations that keep the UI coherent and maintainable.
- **🎨 design-ui-designer** — Crafts pixel-perfect visual designs and component libraries. Turns wireframes into polished UI elements with a keen eye for detail.
- **🛡️ design-brand-guardian** — The guardian of brand integrity. Ensures every visual and textual element aligns with brand guidelines and maintains a cohesive identity.
- **📖 design-visual-storyteller** — Weaves narratives through visuals. Creates compelling information graphics, illustrations, and storyboards that communicate complex ideas simply.
- **✨ design-whimsy-injector** — The spark of joy. Sprinkles delightful micro-interactions, animations, and playful touches that make the product memorable and fun to use.
- **🔍 design-ux-researcher** — The voice of the user. Conducts research, usability tests, and journey mapping to ensure designs are grounded in real user needs and behaviors.
- **♿ design-inclusive-visuals-specialist** — Champions inclusive design. Ensures every visual and interactive element meets WCAG standards and is accessible to users of all abilities.
- **🖼️ design-image-prompt-engineer** — The AI artist. Crafts precise prompts for generative image models to produce custom illustrations, icons, and visual assets on demand.

---

## Pipeline Workflow

The pipeline follows a strict sequential kanban flow. Work items enter at Backlog and progress through each stage gate, with agents handing off completed work to the next agent in the sequence.

```
Backlog → Research → Architecture → Design → Review → Delight → Assets → Done
```

### Stage Details

#### 1. Backlog
- **Owner:** System / Orchestrator
- **Activity:** New design requests are filed as work items in ACMI (`namespace:work`). Each item has a brief, scope, and priority.
- **Entry Criteria:** A design brief exists with clear requirements.
- **Exit Criteria:** Work item is assigned to `design-ux-researcher` with a correlationId.

#### 2. Research (`design-ux-researcher`)
- **Owner:** 🔍 design-ux-researcher
- **Activity:** User research, persona validation, competitor analysis, journey mapping, heuristic evaluation.
- **Entry Criteria:** Work item assigned with brief and scope.
- **Exit Criteria:** Research report complete, user needs documented, research artifacts attached.

#### 3. Architecture (`design-ux-architect`)
- **Owner:** 🏗️ design-ux-architect
- **Activity:** Design system foundations, CSS architecture, responsive layout planning, component tree definition, style guide creation.
- **Entry Criteria:** Research report available with user needs and flows.
- **Exit Criteria:** Architecture spec complete, design tokens defined, component hierarchy mapped, responsive breakpoints established.

#### 4. Design (`design-ui-designer`)
- **Owner:** 🎨 design-ui-designer
- **Activity:** Visual design execution, component library creation, wireframing to polished UI, design token application, prototyping.
- **Entry Criteria:** Architecture spec available with structure and tokens.
- **Exit Criteria:** Visual designs complete, component library populated, prototype ready for review.

#### 5. Review (Parallel)
- **Owners:** 🛡️ design-brand-guardian, 📖 design-visual-storyteller, ♿ design-inclusive-visuals-specialist
- **Activity (Brand Guardian):** Brand guideline compliance check, logo usage audit, voice/tone consistency, visual identity alignment.
- **Activity (Storyteller):** Narrative flow review, information hierarchy check, storyboard coherence, visual communication effectiveness.
- **Activity (Accessibility):** WCAG compliance audit, color contrast verification, screen reader compatibility, accessible typography check, inclusive design review.
- **Entry Criteria:** Visual designs complete and available.
- **Exit Criteria:** All three reviewers pass, consolidated review report generated.

#### 6. Delight (`design-whimsy-injector`)
- **Owner:** ✨ design-whimsy-injector
- **Activity:** Micro-interaction design, animation planning, delight touches, motion graphics, playful UI elements.
- **Entry Criteria:** Design passes review, all three review gates signed off.
- **Exit Criteria:** Delight elements designed, animation specs documented, micro-interactions defined.

#### 7. Assets (`design-image-prompt-engineer`)
- **Owner:** 🖼️ design-image-prompt-engineer
- **Activity:** AI image generation prompts, custom illustrations, icon creation, visual asset production, image optimization.
- **Entry Criteria:** Design is finalized with delight elements integrated.
- **Exit Criteria:** All visual assets generated and delivered, asset inventory populated.

#### 8. Done
- **Owner:** System / Orchestrator
- **Activity:** Final validation, artifact packaging, delivery to stakeholder, work item closed.
- **Entry Criteria:** All assets delivered and approved.
- **Exit Criteria:** Work item marked complete in ACMI, final milestone event logged.

---

## Agent Handoff Protocol

When a work item moves between stages, the sending agent logs a handoff event in ACMI and the receiving agent acknowledges it. This creates a traceable chain of custody for every design decision.

### Handoff Event Contract

Every handoff follows this pattern:

```typescript
// Sender logs completion of their stage
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:<sender-agent-id>",
  kind: "handoff-complete",
  correlationId: "<senderAgentId>HandoffTo<receiverAgentId>-<epochMs>",
  summary: "[handoff-complete @<receiver-agent-id>] <work-item-title> — <handoff-notes>"
)

// Receiver logs acknowledgment and begins work
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:<receiver-agent-id>",
  kind: "handoff-ack",
  correlationId: "<receiverAgentId>Ack<handoffCorrelationId>-<epochMs>",
  summary: "[handoff-ack] Picking up <work-item-title> at <stage-name> stage"
)
```

### Handoff Chain

```
Backlog
  ↓ [orchestrator → design-ux-researcher]
Research (design-ux-researcher)
  ↓ [design-ux-researcher → design-ux-architect]
Architecture (design-ux-architect)
  ↓ [design-ux-architect → design-ui-designer]
Design (design-ui-designer)
  ↓ [design-ui-designer → design-brand-guardian, design-visual-storyteller, design-inclusive-visuals-specialist]
Review (parallel: 3 agents)
  ↓ [all 3 review agents → design-whimsy-injector]
Delight (design-whimsy-injector)
  ↓ [design-whimsy-injector → design-image-prompt-engineer]
Assets (design-image-prompt-engineer)
  ↓ [design-image-prompt-engineer → orchestrator]
Done
```

### Parallel Review Handoff

The Review stage involves 3 agents working in parallel. The handoff protocol for parallel review:

1. `design-ui-designer` hands off to all 3 review agents simultaneously via a single handoff event with `kind: "handoff-complete"` addressed to all three.
2. Each review agent (`design-brand-guardian`, `design-visual-storyteller`, `design-inclusive-visuals-specialist`) acknowledges independently with `kind: "handoff-ack"` and `parentCorrelationId` pointing back to the designer's handoff.
3. As each reviewer completes, they log `kind: "review-pass"` or `kind: "review-fail"` with their findings.
4. The orchestrator waits for all 3 `review-pass` events before advancing to the Delight stage.

### Signal Updates

During handoff, agents should also update their ACMI signals to reflect current state:

```typescript
acmi_signal(
  namespace: "agent",
  id: "<agent-id>",
  signals: JSON.stringify({
    status: "idle" | "working" | "blocked",
    current_work_item: "<work-item-id>",
    current_stage: "<stage-name>"
  })
)
```

---

## Quality Gates

Each pipeline stage has quality gates that must be satisfied before the work item can advance. These gates are checked by the receiving agent upon handoff.

### Quality Gates by Stage

#### Research Gate
- [ ] User personas documented
- [ ] Journey maps created or updated
- [ ] Competitor analysis completed
- [ ] Heuristic evaluation performed
- [ ] Research findings synthesized into actionable recommendations

#### Architecture Gate
- [ ] CSS architecture defined (methodology, naming convention)
- [ ] Design tokens established (colors, typography, spacing, breakpoints)
- [ ] Component hierarchy mapped
- [ ] Responsive layout strategy documented
- [ ] Design system foundations documented

#### Design Gate
- [ ] Visual designs match architecture spec
- [ ] Design tokens applied consistently
- [ ] Component library populated
- [ ] Prototype functional
- [ ] Designs follow platform conventions (iOS, Android, Web)

#### Brand Guardian Gate
- [ ] Brand colors used correctly per guidelines
- [ ] Typography follows brand type scale
- [ ] Logo usage conforms to brand rules
- [ ] Voice and tone consistent with brand
- [ ] Visual identity elements match brand system

#### Storyteller Gate
- [ ] Information hierarchy supports the narrative
- [ ] Visual flow guides the user logically
- [ ] Data visualizations are clear and accurate
- [ ] Illustrations support the story
- [ ] Communication goal is achieved

#### Accessibility Gate
- [ ] WCAG 2.1 AA minimum compliance verified
- [ ] Color contrast ratios meet WCAG thresholds
- [ ] All interactive elements keyboard accessible
- [ ] Screen reader support verified
- [ ] Focus states visible and logical
- [ ] Alt text provided for all images

#### Delight Gate
- [ ] Micro-interactions enhance (not distract)
- [ ] Animations respect reduced-motion preferences
- [ ] Delight elements serve a purpose (not decoration)
- [ ] Transition timings are consistent
- [ ] Haptic/feedback patterns are cohesive

#### Assets Gate
- [ ] All required image assets produced
- [ ] Icons consistent with design system
- [ ] Image resolutions suitable for target displays
- [ ] Asset naming follows conventions
- [ ] Optimized for web delivery

### Gate Failure Protocol

If a quality gate fails:
1. The reviewing agent logs `kind: "review-fail"` with specific reasons
2. The work item is sent back to the originating stage via a `kind: "handback"` event
3. The originating agent addresses findings and re-submits
4. A maximum of 3 rework cycles is allowed before escalation

---

## ACMI Coordination

All agent coordination happens through ACMI. The protocol provides persistent identity (profiles), mutable state (signals), and append-only history (timeline) for every agent and work item.

### ACMI Namespaces Used

| Namespace | Entity Pattern | Purpose |
|-----------|---------------|---------|
| `agent` | `design-<role>` | Agent profiles, signals, timeline |
| `work` | `<work-item-id>` | Work item profiles, signals, timeline |
| `thread` | `design-agency-<topic>` | Coordination threads for team discussions |
| `session` | `<agent-id>:<session-id>` | Agent session tracking |
| `project` | `design-agency-pipeline` | Project-level coordination |

### Agent Profile Structure

Each design agent has the following profile shape in ACMI:

```json
{
  "name": "design-<role>",
  "role": "<role-description>",
  "actor_type": "agent",
  "tenant_id": "madez",
  "compliance": "v1.3-aligned",
  "expertise": ["<skill-1>", "<skill-2>", ...],
  "persona": {
    "avatar": "<emoji>",
    "color": "<hex-color>",
    "description": "<persona-description>"
  }
}
```

### Event Kinds Used in the Pipeline

| Kind | When to Use |
|------|-------------|
| `milestone-shipped` | When a pipeline stage completes successfully |
| `handoff-complete` | When an agent finishes their work and hands to the next agent |
| `handoff-ack` | When the receiving agent acknowledges the handoff and begins work |
| `handback` | When work is sent back to a previous stage (quality gate failure) |
| `review-pass` | When a review agent approves the design |
| `review-fail` | When a review agent identifies issues |
| `work-created` | When a new work item enters the pipeline |
| `work-update` | When a work item has a status change |
| `work-completed` | When a work item reaches Done |
| `decision` | When a design decision is recorded |
| `scope-decision` | When scope changes are decided |
| `coord-note` | For general coordination messages |

### Using acmi_event with milestone-shipped

When a pipeline stage completes, use `kind: 'milestone-shipped'` with the proper `correlationId`:

```typescript
acmi_event(
  namespace: "agent",
  id: "<agent-id>",
  source: "agent:<agent-id>",
  kind: "milestone-shipped",
  correlationId: "<agentId><stageName>Complete-<epochMs>",
  summary: "[milestone-shipped @orchestrator] <stage-name> stage complete for <work-item-title>"
)
```

### Using acmi_signal for State Tracking

Agents update their signals to reflect current status:

```typescript
acmi_signal(
  namespace: "agent",
  id: "<agent-id>",
  signals: JSON.stringify({
    status: "working",
    current_work_item: "<work-item-id>",
    current_stage: "<stage-name>",
    started_at: "<iso-timestamp>",
    progress_pct: 50
  })
)
```

### Bootstrapping an Agent Session

When an agent starts a new session, it should bootstrap first:

```typescript
acmi_spawn(agentId: "<agent-id>", sessionId: "<uuid>", modelId: "<model>")
const context = acmi_bootstrap(agentId: "<agent-id>")
// context contains: profile, signals, recent_timeline, rollup
```

---

## Open Design Daemon Integration

The Design Agency Pipeline integrates with the Open Design daemon for project management and agent lifecycle.

### Project Registration

The project is registered in the Open Design daemon with:
- **Project ID:** `design-agency-pipeline`
- **Project Type:** Pipeline
- **Skills Directory:** `skills/design-agency-playbook/`
- **MCP Configuration:** ACMI MCP server wired via `.od/mcp-config.json`

### Spawning Agents

Agents are spawned through the daemon's API or via ACMI's `acmi_spawn` tool. When spawning a design agent:

1. Call `acmi_spawn` with the agent ID and desired model
2. Call `acmi_bootstrap` to get the agent's full context
3. The agent reads its assigned work item from signals
4. The agent begins work on its pipeline stage

### Work Item Lifecycle

Work items flow through the daemon's work item system:

1. Create: `acmi_work_create(id, profile)` — new design request
2. Assign: Update signals to assign to the next agent
3. Progress: `acmi_work_event` for each milestone
4. Complete: `acmi_work_signal` with status `completed`
5. Archive: Work item marked done in the pipeline

---

## Project Reference

- **Project:** `design-agency-pipeline` (Open Design project ID)
- **Repository:** `/Users/michaelshaw/Projects/open-design`
- **Skill Location:** `skills/design-agency-playbook/`
- **Agent Files:** `skills/design-agency-playbook/agents/`
- **Playbook Files:** `skills/design-agency-playbook/playbook/`
- **ACMI MCP:** Wired via `.od/mcp-config.json`
- **Daemon API:** Open Design daemon

### Agent SKILL.md Files

Each agent has an individual SKILL.md ready to be loaded when that agent is activated:

| Agent | File |
|-------|------|
| design-ux-researcher | `agents/design-ux-researcher.SKILL.md` |
| design-ux-architect | `agents/design-ux-architect.SKILL.md` |
| design-ui-designer | `agents/design-ui-designer.SKILL.md` |
| design-brand-guardian | `agents/design-brand-guardian.SKILL.md` |
| design-visual-storyteller | `agents/design-visual-storyteller.SKILL.md` |
| design-whimsy-injector | `agents/design-whimsy-injector.SKILL.md` |
| design-inclusive-visuals-specialist | `agents/design-inclusive-visuals-specialist.SKILL.md` |
| design-image-prompt-engineer | `agents/design-image-prompt-engineer.SKILL.md` |

### Playbook Files

Detailed workflow definitions:

| File | Description |
|------|-------------|
| `playbook/pipeline-flow.md` | Full pipeline workflow with stage details |
| `playbook/handoff-protocol.md` | Agent handoff protocol in detail |
| `playbook/quality-gates.md` | Per-stage quality gates and gate failure procedures |

---

## Quick Start

1. **Create a work item:** Use `acmi_work_create` with a design brief as profile
2. **Assign to Research:** Signal `design-ux-researcher` with the work item ID
3. **Follow the handoff chain:** Each agent completes their stage and hands off
4. **Monitor progress:** Use `acmi_cat` to view the work item timeline
5. **Complete:** When the item reaches Done, log the final milestone

```typescript
// Example: Creating a new work item
acmi_work_create(
  id: "homepage-redesign-2026-001",
  profile: JSON.stringify({
    title: "Homepage Redesign",
    description: "Redesign the company homepage with new brand guidelines",
    priority: "high",
    requester: "@mikey",
    created_at: "2026-05-23T00:00:00Z"
  })
)
```
