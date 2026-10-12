# Design Agency CLI Tools

CLI wrapper for spawning the Design Agency daemon agent.

## Setup

The daemon must be running. Start it with:

```bash
od daemon start
# or
pnpm tools-dev
```

## Usage

```bash
# Full-stack agency (default)
./run.sh "Design a landing page for a fintech startup"

# Role-specific
./run.sh --role=ui "Design the onboarding flow"
./run.sh --role=brand "Create a brand identity system"
./run.sh --role=creative "Concept a campaign for a new product"
./run.sh --role=content "Write copy for a landing page"
./run.sh --role=designer "Build a design system in code"

# With model override
./run.sh --role=brand --model=anthropic/claude-sonnet-4-5 \
  "Audit and refresh the brand palette"

# Override daemon port
OD_DAEMON_PORT=17500 ./run.sh --role=ui "Design the dashboard"
```

## Available roles

| Role        | Description                               |
|-------------|-------------------------------------------|
| full-stack  | All design capabilities combined (default)|
| ui          | UI/UX Designer                            |
| brand       | Brand Designer                            |
| content     | Content Strategist                        |
| creative    | Creative Director                         |
| designer    | Design Engineer (code-first)              |

## Requirements

- `curl` — for HTTP requests to the daemon API
- `jq` — for JSON construction and response parsing
- Open Design daemon running on `http://127.0.0.1:17456` (or `OD_DAEMON_PORT`)
