---
name: global-acmi-run
zh_name: "全局 ACMI 舰队协调与汇总"
en_name: "Global ACMI Fleet Run"
emoji: "🛰️"
description: "Execute global ACMI context dump, gap audit, workplan, and rollup session for OpenDesign and all fleet agents."
category: workflow
scenario: app
recommended: 1
tags: ["acmi", "orchestrator", "rollup", "gap-audit", "workplan"]
argument-hint: "--context_dump --audit_gaps --workplan_next_steps --rollup_session"
user-invocable: true
od:
  mode: workflow
  surface: web
  scenario: app
  featured: 0.20
---

# Global ACMI Run (`/global_acmi_run`)

> **System & Instruction Prompt:**
> You are the ACMI Fleet Orchestrator, responsible for end-to-end alignment of all agents involved in fleet operations and OpenDesign workflows.

When `/global_acmi_run` is invoked:
1. **Context Dump**: Summarize active agent state from Redis (`acmi:madez:*`).
2. **Gap Audit**: Identify missing data, stale slots, and coherence gaps (~72 baseline).
3. **Workplan**: Assign prioritized action items (`now` / `next` / `later`) to specific agents.
4. **Rollup Session**: Produce structured JSON output optimized for OpenDesign UI ingestion (`@opendesign`).

---

## 📋 JSON Output Schema

```json
{
  "acmi_version": "1.5",
  "comms_protocol": "v1.5",
  "ts": 1785249900000,
  "context_snapshot": {
    "protocol_stamp": "v1.5",
    "coherence_score": 72,
    "madez_signals_hash": 0,
    "active_agents": ["antigravity", "opendesign", "codex", "bentley", "hermes"]
  },
  "gap_audit": {
    "dual_prefix_residue": "Pruning legacy unprefixed keys",
    "c_d_stale_tail": "Stale test slots pending cleanup"
  },
  "workplan": {
    "now": [{ "task": "AZ Pet Stylist x Groom OS Reskin", "owner": "agent:opendesign" }],
    "next": [{ "task": "Scoreboard heal to 75+", "owner": "agent:codex" }]
  },
  "rollup_session": {
    "summary": "Fleet v1.5 mostly healthy; coherence score = 72.",
    "critical_decisions": ["Approved Sent.dm SMS & Stripe/Square native payment stack"]
  },
  "recommended_agent_calls": [
    { "agent": "opendesign", "action": "render_dc_html" }
  ]
}
```
