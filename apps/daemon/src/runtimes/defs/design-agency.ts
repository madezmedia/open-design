import { DEFAULT_MODEL_OPTION } from './shared.js';
import type { RuntimeAgentDef } from '../types.js';

/**
 * Design Agency — spawnable design agent that wraps the Hermes ACP runtime
 * with design-agency context injected via environment variables.
 *
 * How it works:
 * 1. Uses `hermes` as the actual CLI backend (ACP protocol, mature ACMI MCP support)
 * 2. Sets env vars that the daemon's prompt system reads to inject design-agency
 *    playbook content into the system prompt (see prompts/system.ts)
 * 3. The orchestrator SKILL.md at skills/design-agent-orchestrator/ tells the
 *    agent how to activate the correct design role based on ACMI profile/signals
 * 4. ACMI MCP tools are available via `mcpDiscovery: 'mature-acp'`
 *
 * Usage:
 *   od run design-agency "Design a landing page for..."
 *
 * Role selection (set via env before spawning):
 *   OD_DESIGN_ROLE=ui        -> UI/UX designer
 *   OD_DESIGN_ROLE=brand     -> Brand identity designer
 *   OD_DESIGN_ROLE=content   -> Content/copy strategist
 *   OD_DESIGN_ROLE=creative  -> Creative director / art director
 *   (default: full-stack design agency — all roles)
 *
 * When ACMI is connected, the agent reads its ACMI profile to determine
 * which design role to activate automatically.
 */
export const designAgencyAgentDef = {
  id: 'design-agency',
  name: 'Design Agency',
  // Uses the Hermes ACP runtime as the actual CLI backend — no separate
  // binary needed. Hermes was chosen because it supports the ACP protocol
  // (mature-acp MCP discovery), has built-in ACMI hooks via --accept-hooks,
  // and is available on PATH wherever Open Design is installed.
  bin: 'hermes',
  fallbackBins: ['opencode-cli', 'opencode'],
  versionArgs: ['--version'],
  // ACMI MCP tools are required for reading design agency profile/signals.
  // 'mature-acp' triggers the daemon's live-artifacts MCP server injection
  // (see mcp.ts: buildLiveArtifactsMcpServersForAgent).
  mcpDiscovery: 'mature-acp',
  // Environment variables the daemon reads when composing the system prompt.
  // The prompt system (system.ts) checks OD_DESIGN_* vars and injects the
  // corresponding design agency playbook content.
  env: {
    OD_DESIGN_AGENCY: '1',
    OD_DESIGN_ROLE: 'full-stack',
    OD_DESIGN_PLAYBOOK: 'design-agent-orchestrator',
  },
  // Use Hermes ACP mode — sends/receives structured JSON-RPC over stdio.
  // --accept-hooks enables the built-in ACMI hook support so the agent can
  // bootstrap from ACMI on session start.
  // No custom fetch/list models — falls back to agent-level resolution
  // Fallback models optimized for design work — Claude Sonnet (best UI/UX
  // reasoning), Gemini 2.5 Pro (multimodal + long context for brand audits),
  // and GPT-5.5 (strong creative direction).
  fallbackModels: [
    DEFAULT_MODEL_OPTION,
    { id: 'anthropic/claude-sonnet-4-5', label: 'Claude Sonnet 4.5 (best for design work)' },
    { id: 'google/gemini-2.5-pro', label: 'Gemini 2.5 Pro (brand audits, long context)' },
    { id: 'openai/gpt-5.5', label: 'GPT-5.5 (creative direction)' },
    { id: 'anthropic/claude-opus-4-5', label: 'Claude Opus 4.5 (design critique)' },
    { id: 'deepseek-v4-flash', label: 'DeepSeek V4 Flash (fast iteration)' },
  ],
  // Prompt is delivered via ACP protocol — hermes reads the prompt from
  // stdin as a JSON-RPC message. This avoids argv length limits.
  buildArgs: (
    _prompt,
    _imagePaths,
    _extraAllowedDirs = [],
    options = {},
  ) => {
    const args = ['acp', '--accept-hooks'];
    if (options.model && options.model !== 'default') {
      args.push('--model', options.model);
    }
    return args;
  },
  streamFormat: 'acp-json-rpc',
  // Install/docs URLs pointing at the design agency documentation
  installUrl: 'https://github.com/madezmedia/hermes-cli',
  docsUrl: 'https://github.com/michaelshaw/open-design/docs/design-agency-integration.md',
} satisfies RuntimeAgentDef;
