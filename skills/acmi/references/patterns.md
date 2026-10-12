# ACMI Patterns — Worked Recipes

The standard fleet coordination recipes, updated and aligned with **ACMI v1.4** and **Protocol 9 (Git Atomic Git Sync)**.

## Table of contents

1. Bootstrap-on-spawn
2. Milestone with correlationId chain
3. Cross-agent handoff
4. Session-end rollup
5. Heartbeats (anti-dead)
6. RL signal via logAssessment
7. Lock protocol (optimistic locking)
8. Fleet discovery via registry
9. HITL queues (per-actor in v1.3/v1.4)
10. Incident chaining
11. Work item lifecycle
12. Multi-stream `acmi_cat` for fleet dashboards
13. **Protocol 9 — Git Atomic Git Sync**

---

## 1. Bootstrap-on-spawn

**Why.** A fresh agent session that doesn't read prior state is going to repeat decisions, contradict yesterday's conclusions, and miss handoffs addressed to it.

**Recipe.**
```
1. acmi_spawn(agentId="claude-engineer", modelId="claude-opus-4-7")
2. ctx = acmi_bootstrap(agentId="claude-engineer")
3. Read in this order:
   a. ctx.rollup            — what did the previous session decide?
   b. ctx.active_threads    — what coordination is live?
   c. ctx.recent_timeline   — what just happened?
   d. ctx.signals           — what's the current state?
   e. ctx.profile           — who am I?
4. Optional: acmi_cat(keys=ctx.active_threads, since="6h")
   to fold in cross-thread context.
```

---

## 2. Milestone with correlationId chain

**Why.** Without correlationIds, your event is an orphan. Nobody can chain off it, nobody can trace where a decision came from, and your timeline becomes unreadable past 50 events.

**Recipe.** Generate a descriptive camelCase prefix; suffix with `Date.now()`-style ms epoch.
```
correlationId = f"claudeEngineerSmitheryQualityWin-{int(time.time()*1000)}"
acmi_event(
  namespace="agent", id="claude-engineer",
  source="agent:claude-engineer",
  kind="milestone-shipped",
  correlationId=correlationId,
  summary="[milestone-shipped @bentley @mikey] Smithery quality score reached 83 (target 90)"
)
```

---

## 3. Cross-agent handoff

**Why.** Agents in a fleet drop work across sessions. Without an explicit handoff event, the receiver has no signal that they own a thing.

**Recipe.**
```
# SENDER
acmi_event(
  namespace="thread", id="agent-coordination",
  source="agent:bentley",
  kind="task-delegation",
  correlationId="bentleyHandoffSmitheryDebug-<ts>",
  summary="[task-delegation @claude-engineer] Smithery scan failing 'serverInfo null' — debug + ship fix",
)

# RECEIVER (next session, after acmi_bootstrap)
acmi_event(
  namespace="thread", id="agent-coordination",
  source="agent:claude-engineer",
  kind="handoff-ack",
  correlationId="engineerAckBentleySmithery-<ts>",
  parentCorrelationId="bentleyHandoffSmitheryDebug-<ts>",
  summary="[handoff-ack @bentley] picking up Smithery scan debug, eta 30m",
)
```

---

## 4. Session-end rollup

**Why.** The next session's `acmi_bootstrap` reads the rollup. A good rollup is the difference between a fresh session that resumes mid-thought and one that re-derives everything.

**Recipe.**
```python
acmi_rollup_set(
  agentId="claude-engineer",
  rollup=json.dumps({
    "session_summary": "Shipped Smithery configSchema fix (PR#21). Quality score 83→ ?",
    "decisions_made": [
      {"id": "use-stdio-not-http", "rationale": "...", "cid": "..."},
    ],
    "open_blockers": [
      "Mikey verify form renders in incognito (smithery-specialist trigger #1)",
    ],
    "next_session_priorities": [
      "1. Re-run quality scan, target 90+",
      "2. Pair with bentley on listing copy",
    ],
    "key_correlation_ids": [
      "claudeEngineerSmitheryQualityWin-1778174324664",
    ],
    "session_duration_min": 47,
  })
)
```

---

## 5. Heartbeats (anti-dead)

**Why.** Long-running agents go dark. Without a heartbeat, fleet dashboards can't tell "asleep deliberately" from "crashed". Also makes the dashboard feel alive.

**Recipe.** A periodic `kind: heartbeat` event on the agent's own timeline.
```
acmi_event(
  namespace="agent", id="drift-remediator",
  source="agent:drift-remediator",
  kind="heartbeat",
  correlationId="driftHeartbeat-<ts>",
  summary="[heartbeat] alive, last sweep 0 issues",
)
```

---

## 6. RL signal via `logAssessment`

**Why.** Closing the loop on agent reward signal — was the work good? — by encoding a 0–100 score on completion events. The fleet's RL engine pulls from these.

**Recipe.** On any `kind: *-completed` or `*-shipped` event, include `payload.logAssessment`:
```
acmi_event(
  namespace="work", id="acmi-skill-syndication",
  source="agent:claude-engineer",
  kind="work-completed",
  correlationId="...",
  summary="[work-completed @mikey] Skill packaged + 3 syndication targets ready",
)
```

---

## 7. Lock protocol (optimistic locking)

**Why.** Two agents writing the same signal at the same time will overwrite each other. For state that needs ordering (a deploy slot, a singleton task), wrap writes in optimistic locks.

**Recipe.** Read with version → mutate → write with version assertion.
```
1. ctx = acmi_get(namespace="thread", id="deploy-slot")
2. version = ctx.signals.get("version", 0)
3. If ctx.signals.get("locked_by") and ctx.signals.get("locked_by") != self:
     bail — someone else holds the lock
4. acmi_signal(
     namespace="thread", id="deploy-slot",
     signals=json.dumps({"locked_by": self, "version": version + 1, "locked_at": now()})
   )
5. Verify with acmi_get; if version is now version+1 and locked_by==self, you have the lock
6. Do the work
7. Release: acmi_signal(..., signals=json.dumps({"locked_by": null, "version": version + 2}))
```

---

## 8. Fleet discovery via registry

**Why.** New agents joining a fleet need to know who's out there. The registry pattern stores per-agent metadata in a known location.

**Recipe.** A profile under `acmi:registry:fleet:<agentId>` for each agent:
```
acmi_profile(
  namespace="registry",
  id="fleet:claude-engineer",
  profile=json.dumps({
    "actor_type": "agent",
    "fleet_role": "RL Engine + Primary Coder",
    "primary_threads": ["agent-coordination", "newsroom"],
    "skills": ["typescript", "redis", "smithery-debug"],
    "wake_window_utc": "00:00-23:59",
    "primary_id": "claude-engineer",
  })
)
```

---

## 9. HITL queues (per-actor in v1.3/v1.4)

**Why.** Some events require a human-in-the-loop decision before the fleet proceeds. v1.2 had one shared queue; v1.3/v1.4 adds per-actor queues so a question for Mikey doesn't block on a question for Duane.

**Recipe.** When an agent needs human input:
```
# Push to per-human queue (v1.3/v1.4)
acmi_event(
  namespace="hitl", id="user:mikey:open",
  source="agent:claude-engineer",
  kind="hitl-required",
  correlationId="needMikeyDecideRepoBoundary-<ts>",
  summary="[hitl-required @mikey] Pick option 1, 2, or 3 from acmi-repo-architecture-decision",
)
```

---

## 10. Incident chaining

**Why.** Incidents (outages, secret leaks, degradations) generate dozens of events from many sources. A single root `correlationId` makes them re-readable.

**Recipe.** Open with one event, chain everything to it via `parentCorrelationId`:
```
acmi_event(
  namespace="thread", id="agent-coordination",
  source="agent:claude-engineer",
  kind="incident-opened",
  correlationId="incident-secrets-leak-acmi-protocol-repo-1778419629871",
  summary="[incident-opened P0] secrets leaked in acmi-protocol-repo, privatized 13:25Z",
)
```

---

## 11. Work item lifecycle

**Why.** Work items capture cross-session projects. Use the dedicated `acmi_work_*` tools rather than raw `acmi_event` so the work-item-aware UIs (ops-center, dashboards) light up.

**Recipe.**
```
# 1. Create
acmi_work_create(id="acmi-skill-syndication", profile=...)

# 2. Update signals
acmi_work_signal(id="acmi-skill-syndication", signals='{"draft_status":"WRITTEN","tested":false}')

# 3. Log progress events
acmi_work_event(
  id="acmi-skill-syndication",
  source="agent:claude-engineer",
  summary="[work-update] Draft SKILL.md complete, evals next"
)
```

---

## 12. Multi-stream `acmi_cat` for fleet dashboards

**Why.** A fleet dashboard wants the merged firehose, not 30 separate timeline reads.

**Recipe.**
```
events = acmi_cat(
  keys=[
    "thread:agent-coordination",
    "thread:newsroom",
    "agent:claude-engineer",
    "agent:bentley",
    "agent:claude-web",
  ],
  since="24h",
  limit=200
)
```

---

## 13. Protocol 9 — Git Atomic Git Sync

**Why.** Forces branch synchronization and atomic commit auditing for fleet agents working on the same repository to eliminate merge conflicts.

**Recipe.**
```
# 1. Acquire the repository branch lock
acmi_signal(
  namespace="thread", id="git-sync",
  signals='{"locked_by": "agent:claude-engineer", "branch": "main", "locked_at": 1778423299460}'
)

# 2. Perform atomic modifications and commit locally
#    Git commit -m "feat: setup NextJS components (atomic-sync-1778423299460)"

# 3. Append commit notification event to timeline
acmi_event(
  namespace="thread", id="git-sync",
  source="agent:claude-engineer",
  kind="git-commit-pushed",
  correlationId="gitSyncMainCommit-1778423299460",
  summary="[git-commit-pushed @fleet] branch 'main', commit '8c105ab', correlationId: gitSyncMainCommit-1778423299460",
  speaker_type="agent"
)

# 4. Release branch lock
acmi_signal(
  namespace="thread", id="git-sync",
  signals='{"locked_by": null, "branch": "main"}'
)
```
