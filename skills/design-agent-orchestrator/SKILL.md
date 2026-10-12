---
name: design-agent-orchestrator
description: >
  Multi-role design agency orchestration. Spawns the design-agency daemon agent
  and activates the correct design role based on ACMI profile/signals. Supports
  UI/UX, brand identity, content strategy, and creative direction roles.
  Triggers include "design agency", "design team", "spawn designer",
  "activate design role", "full-stack design".
triggers:
  - "design agency"
  - "design team"
  - "spawn designer"
  - "activate design role"
  - "full-stack design"
  - "ui/ux design"
  - "brand identity"
  - "creative direction"
  - "content strategy"
od:
  mode: utility
  category: creative-direction
  requires:
    - acmi
---

# Design Agent Orchestrator

Orchestrate design work across multiple specialized design roles. This skill
is the bridge between the daemon's `design-agency` agent type and ACMI's
profile/signal system for role activation.

## How it works

The Design Agency agent (`od run design-agency "..."`) wraps the Hermes ACP
runtime with design-context environment variables. When launched, it:

1. **Bootstraps from ACMI** — Calls `acmi_bootstrap("design-agency")` to
   load its profile (role configuration, preferences, brand context) and
   signals (current task, active project, mood/energy).
2. **Activates the correct design role** — Reads `OD_DESIGN_ROLE` env var
   or ACMI profile `role` field to determine which design persona to adopt.
3. **Loads the design playbook** — Uses the design-agent-orchestrator skill
   body (this file) as its operating playbook, plus any active skill or
   design system bound to the daemon run.
4. **Connects design tools** — Through `mcpDiscovery: mature-acp`, the
   agent gets access to:
   - ACMI MCP tools (profile/signals/timeline read/write)
   - Open Design live artifacts MCP (design system tokens, previews)
   - Filesystem and shell tools (via the Hermes/OpenCode runtime)

## Design roles

The design-agency agent supports these roles. Set `OD_DESIGN_ROLE` or ACMI
profile `role` before spawning:

| Role ID     | Label               | Focus area                                    |
|-------------|---------------------|-----------------------------------------------|
| `full-stack`| Full-Stack Agency   | All roles (default)                           |
| `ui`        | UI/UX Designer      | Interface design, interaction, user flows     |
| `brand`     | Brand Designer      | Identity, palette, typography, logo systems   |
| `content`   | Content Strategist  | Copy, messaging, content architecture         |
| `creative`  | Creative Director   | Art direction, concept, campaign strategy     |
| `designer`  | Design Engineer     | Code-first design, design systems, CSS/React  |

### Role behavior

Each role gets a tailored system prompt section that the daemon injects
based on `OD_DESIGN_ROLE`. The role shapes:

- **Tool preference** — UI roles lean on design tools; content roles lean
  on writing/editing tools.
- **Output style** — Creative directors produce briefs and moodboards;
  design engineers produce code and design tokens.
- **Review criteria** — Each role has its own critique dimensions (UI
  critiques layout/interaction; brand critiques consistency/identity).

## ACMI integration

The design-agency agent uses ACMI for persistent context across sessions:

```
# On first spawn, set up the agent profile
acmi_profile(
  namespace="agent", id="design-agency",
  profile=json.dumps({
    "name": "Design Agency",
    "role": "full-stack",
    "brands": [],
    "preferred_models": ["anthropic/claude-sonnet-4-5"],
    "actor_type": "agent"
  })
)

# Before each session, bootstrap
context = acmi_bootstrap("design-agency")
# context contains: profile, signals, timeline, rollup

# Log milestones
acmi_event(
  namespace="agent", id="design-agency",
  source="agent:design-agency",
  kind="milestone-shipped",
  correlationId="agencyDesignSystemLaunch-<ts>",
  summary="[milestone-shipped] Shipped complete design system"
)

# Roll up at session end
acmi_rollup_set(
  agentId="design-agency",
  rollup=json.dumps({
    "session_summary": "Completed brand identity for FinTech client",
    "decisions_made": ["Palette: navy/white with coral accent",
                       "Typography: Inter + Space Grotesk"],
    "open_blockers": ["Awaiting logo feedback from stakeholder"],
    "next_session_priorities": ["Finalize component library"]
  })
)
```

## Spawning design agents

### Via the daemon API

```bash
# Default (full-stack agency)
od run design-agency "Design a landing page for a fintech startup"

# UI/UX specialist
OD_DESIGN_ROLE=ui od run design-agency "Design the onboarding flow"

# Creative director mode
OD_DESIGN_ROLE=creative od run design-agency "Concept a brand campaign"
```

### Via the CLI tool

```bash
# Using the design-agency CLI wrapper
tools/design-agency/run.sh --role=ui "Redesign the dashboard"
tools/design-agency/run.sh --role=brand "Create a brand identity"
```

### Via the web UI

1. Open the daemon web UI
2. In the agent selector, choose "Design Agency"
3. (Optional) Set role via Settings → Agent Config → Design Role
4. Type your design request in the chat

## Available design skills

When acting as a design agency, these companion skills are available to
delegate to or reference:

| Skill                  | Purpose                                |
|------------------------|----------------------------------------|
| `design-brief`         | Parse structured briefs into DESIGN.md |
| `design-review`        | Visual audit + fixes with screenshots  |
| `design-consultation`  | Full design system from scratch        |
| `design-md`            | Create/manage DESIGN.md token files    |
| `creative-director`    | Campaign concepts, Cannes review       |
| `color-expert`         | Color palette expertise                |
| `brand-guidelines`     | Brand identity systems                 |
| `taste-skill`          | Anti-slop design taste                 |
| `web-design-guidelines`| Web design best practices              |
| `ui-ux-pro-max`        | Advanced UI/UX patterns                |
| `theme-factory`        | Design token/theme generation          |
| `apple-hig`            | Apple HIG compliance                   |
| `acmi`                 | Persistent context management          |

Each skill is independently listed under `/api/skills` and can be
bound to a run like any other Open Design skill.

## Example workflow

1. **Brief intake** — User says "I need a fintech landing page"
2. **Role activation** — Agent reads ACMI profile, activates `full-stack`
   (or a specific role if `OD_DESIGN_ROLE` is set)
3. **Design brief** — Uses `design-brief` skill to parse the request into
   a structured DESIGN.md with palette, typography, layout, mood, density
4. **Creative exploration** — Creative director role generates 3 visual
   directions with mood references
5. **Execution** — UI designer role builds the actual landing page with
   code, applying the design tokens from step 3
6. **Review** — Uses `design-review` skill for visual audit, before/after
7. **Rollup** — Logs milestone event and session summary to ACMI

## Persistence

All design agency state (active projects, brand contexts, client
preferences, design decisions) is stored in ACMI under the
`agent:design-agency` entity. Starting a new session with
`acmi_bootstrap("design-agency")` restores full context, so the
agency never loses track of in-progress work.
