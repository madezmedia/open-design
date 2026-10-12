# Design Agency Integration

The Design Agency is a spawnable agent type in the Open Design daemon
that wraps the Hermes ACP runtime with design-context environment
variables. It gives you a specialized design agent that can activate
different design roles (UI/UX, brand, content, creative direction)
based on ACMI profile/signals.

## Quick start

```bash
# List available agents (design-agency should appear)
od agents list

# Spawn the design agency
od run design-agency "Design a landing page for a fintech startup"

# Spawn with a specific role
OD_DESIGN_ROLE=ui od run design-agency "Design the onboarding flow"
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Daemon Registry (registry.ts)                      │
│  ┌─────────────────────────────────────────────────┐│
│  │ design-agency def                               ││
│  │  - bin: hermes (ACP runtime)                    ││
│  │  - mcpDiscovery: mature-acp                     ││
│  │  - env: OD_DESIGN_*, role context               ││
│  │  - streamFormat: acp-json-rpc                   ││
│  └─────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────┐│
│  │ Other agents (claude, codex, gemini, etc.)      ││
│  └─────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────┤
│  Skills Directory                                   │
│  ┌─────────────────────────────────────────────────┐│
│  │ skills/design-agent-orchestrator/SKILL.md       ││
│  │  - Role orchestration playbook                  ││
│  │  - ACMI bootstrap workflow                      ││
│  │  - Design role definitions                      ││
│  └─────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────┤
│  ACMI (Agentic Context Memory Interface)            │
│  ┌─────────────────────────────────────────────────┐│
│  │ agent:design-agency                             ││
│  │  - Profile: role, brands, preferences           ││
│  │  - Signals: current task, active project        ││
│  │  - Timeline: session history, milestones        ││
│  │  - Rollup: cross-session summaries              ││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

### How it works

1. **Agent definition** (`apps/daemon/src/runtimes/defs/design-agency.ts`):
   - Uses `hermes` as the CLI backend (no separate binary needed)
   - Sets `mcpDiscovery: 'mature-acp'` so ACMI MCP tools are injected
   - Passes `OD_DESIGN_*` env vars for role configuration
   - Falls back to `opencode-cli` / `opencode` if Hermes isn't installed

2. **Skill playbook** (`skills/design-agent-orchestrator/SKILL.md`):
   - Tells the agent how to bootstrap from ACMI
   - Defines the 6 design roles and their behavior
   - Lists companion skills for delegation
   - Provides ACMI event/rollup workflow

3. **ACMI persistence** (via `@madezmedia/acmi-mcp` MCP server):
   - Agent profile stores role, brand context, preferences
   - Signals track current task, project, mood
   - Timeline logs milestones, decisions, handoffs
   - Rollups carry context across sessions

## Design roles

| Role ID       | Label               | Focus                                         |
|---------------|---------------------|-----------------------------------------------|
| `full-stack`  | Full-Stack Agency   | All design capabilities combined (default)    |
| `ui`          | UI/UX Designer      | Interface design, interaction patterns, flows |
| `brand`       | Brand Designer      | Identity, palette, typography, logo systems   |
| `content`     | Content Strategist  | Copy, messaging, content architecture         |
| `creative`    | Creative Director   | Art direction, concept, campaign strategy     |
| `designer`    | Design Engineer     | Code-first design, design systems, CSS/React  |

Set the role via:
- **Environment variable**: `OD_DESIGN_ROLE=<role-id>` before spawning
- **ACMI profile**: Set `role` field in `agent:design-agency` profile
- **Web UI**: Settings → Agent Config → Design Role (when implemented)

## ACMI integration

The design agency relies on ACMI for persistent memory. Set up the
agent profile once:

```bash
# Install ACMI MCP tools if not already done
npm install -g @madezmedia/acmi-mcp
# Configure UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN

# Create the design-agency agent profile
# (use the ACMI MCP tools available to your current agent)
# acmi_profile(namespace="agent", id="design-agency", profile=json)
```

Then each session starts with `acmi_bootstrap("design-agency")` which
loads profile + signals + recent timeline + rollup in one call.

## Companion skills

These skills are designed to work alongside the design agency agent.
They can be bound to a run or invoked by the agent:

- **design-brief** — Parse structured I-Lang briefs into DESIGN.md
- **design-review** — Visual audit with before/after screenshots
- **design-consultation** — Full design system from scratch
- **creative-director** — Campaign concepts with Cannes/D&AD review
- **color-expert** — Color palette expertise and accessibility
- **taste-skill** — Anti-slop design taste (tunable variance/density)
- **theme-factory** — Design token and theme generation

## Running design agents

### From CLI

```bash
# Full-stack agency mode (default)
od run design-agency "Design a landing page"

# UI/UX specialist
OD_DESIGN_ROLE=ui od run design-agency "Design the dashboard"

# Creative director
OD_DESIGN_ROLE=creative od run design-agency "Concept a campaign"

# With a specific model
OD_DESIGN_ROLE=brand od run design-agency --model anthropic/claude-sonnet-4-5 \
  "Create a brand identity for a coffee shop"
```

### Using the CLI wrapper tool

```bash
# Run with role selection
tools/design-agency/run.sh --role=ui "Redesign the checkout flow"

# Override the model
tools/design-agency/run.sh --role=brand --model=gemini-2.5-pro \
  "Audit and redesign the brand palette"
```

### From the daemon API

```bash
curl -X POST http://localhost:17456/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "design-agency",
    "env": { "OD_DESIGN_ROLE": "ui" },
    "prompt": "Design the onboarding flow for a fintech app"
  }'
```

## Files reference

| File | Purpose |
|------|---------|
| `apps/daemon/src/runtimes/defs/design-agency.ts` | Agent definition (registry entry) |
| `apps/daemon/src/runtimes/registry.ts` | Agent registry (imports + registers) |
| `skills/design-agent-orchestrator/SKILL.md` | Orchestration playbook skill |
| `docs/design-agency-integration.md` | This documentation |
| `tools/design-agency/run.sh` | CLI wrapper script |

## Extending

To add a new design role, edit:
1. `skills/design-agent-orchestrator/SKILL.md` — Add role to the table
   and define its behavior
2. `apps/daemon/src/runtimes/defs/design-agency.ts` — If the role needs
   specific env vars or fallback models

To add a new companion skill, follow the `skills/AGENTS.md` instructions
for creating a skill stub. The design agency will discover it via
`/api/skills`.
