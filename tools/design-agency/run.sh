#!/usr/bin/env bash
#
# design-agency-runner — CLI wrapper for the Design Agency daemon agent
#
# Spawns the design-agency agent with role selection, model overrides,
# and optional ACMI bootstrap integration.
#
# Usage:
#   ./run.sh --role=<role> [--model=<model>] [--help] <prompt>
#
# Examples:
#   ./run.sh --role=ui "Redesign the dashboard onboarding flow"
#   ./run.sh --role=brand --model=anthropic/claude-sonnet-4-5 \
#     "Create brand identity for a coffee shop"
#   ./run.sh "A full landing page design"   # defaults to full-stack
#
# Environment variables:
#   OD_DAEMON_PORT  — Daemon HTTP port (default: 17456)
#   OD_DESIGN_ROLE  — Design role override (default: full-stack)

set -euo pipefail

# ── Configuration ────────────────────────────────────────────
OD_DAEMON_PORT="${OD_DAEMON_PORT:-17456}"
OD_DESIGN_ROLE="${OD_DESIGN_ROLE:-full-stack}"
DESIGN_AGENCY_API="http://127.0.0.1:${OD_DAEMON_PORT}"

# ── Parse arguments ──────────────────────────────────────────
ROLE=""
MODEL=""
PROMPT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --role=*)
      ROLE="${1#*=}"
      shift
      ;;
    --role)
      ROLE="$2"
      shift 2
      ;;
    --model=*)
      MODEL="${1#*=}"
      shift
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 [--role=<role>] [--model=<model>] <prompt>"
      echo ""
      echo "Design roles:"
      echo "  full-stack  — Full-Stack Agency (all design capabilities)"
      echo "  ui          — UI/UX Designer (interface, interaction)"
      echo "  brand       — Brand Designer (identity, palette)"
      echo "  content     — Content Strategist (copy, messaging)"
      echo "  creative    — Creative Director (art direction, concepts)"
      echo "  designer    — Design Engineer (code-first design)"
      echo ""
      echo "Examples:"
      echo "  $0 --role=ui \"Redesign the onboarding flow\""
      echo "  $0 --role=brand --model=anthropic/claude-sonnet-4-5 \"Brand\""
      exit 0
      ;;
    -*)
      echo "Unknown option: $1"
      echo "Usage: $0 [--role=<role>] [--model=<model>] <prompt>"
      exit 1
      ;;
    *)
      PROMPT="$*"
      break
      ;;
  esac
done

if [[ -z "$PROMPT" ]]; then
  echo "Error: No prompt provided. Pass a design prompt as the final argument."
  echo "Usage: $0 [--role=<role>] [--model=<model>] <prompt>"
  exit 1
fi

# Validate role
VALID_ROLES=("full-stack" "ui" "brand" "content" "creative" "designer")
if [[ -n "$ROLE" ]]; then
  OD_DESIGN_ROLE="$ROLE"
fi
IS_VALID=0
for r in "${VALID_ROLES[@]}"; do
  if [[ "$OD_DESIGN_ROLE" == "$r" ]]; then
    IS_VALID=1
    break
  fi
done
if [[ "$IS_VALID" -eq 0 ]]; then
  echo "Error: Invalid role '$OD_DESIGN_ROLE'. Valid roles: ${VALID_ROLES[*]}"
  exit 1
fi

# ── Check daemon health ──────────────────────────────────────
if ! curl -sf "${DESIGN_AGENCY_API}/api/health" > /dev/null 2>&1; then
  echo "Error: Open Design daemon not reachable at ${DESIGN_AGENCY_API}"
  echo "Start the daemon first with: od daemon start  (or pnpm tools-dev)"
  exit 1
fi

# ── Build and send request ───────────────────────────────────
echo "🎨 Design Agency — Role: ${OD_DESIGN_ROLE}"
if [[ -n "$MODEL" ]]; then
  echo "   Model: ${MODEL}"
fi
echo ""
echo "📝 Prompt: ${PROMPT}"
echo "─────────────────────────────────────────────"

# Build request body
BODY=$(jq -n \
  --arg prompt "$PROMPT" \
  --arg role "$OD_DESIGN_ROLE" \
  --arg model "$MODEL" \
  '{
    agent: "design-agency",
    env: { OD_DESIGN_ROLE: $role },
    prompt: $prompt
  } | if $model != "" then . + { model: $model } else . end')

# Send the request and stream the response
curl -N -X POST "${DESIGN_AGENCY_API}/api/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d "$BODY" 2>&1 | while IFS= read -r line; do
  # Strip SSE "data: " prefix and pretty-print
  case "$line" in
    "data: "*)
      content="${line#data: }"
      # Attempt to extract text from JSON SSE events
      echo "$content" | jq -r '.text // .content // .message // .' 2>/dev/null || echo "$content"
      ;;
    *)
      # Skip SSE comments and empty lines
      ;;
  esac
done

echo ""
echo "─────────────────────────────────────────────"
echo "✅ Design session complete"
