# Handoff Protocol

> Part of the Design Agency Playbook — defines how agents pass work between pipeline stages.

## Overview

Handoffs are the mechanism by which work moves through the Design Agency Pipeline. Each handoff creates a traceable event chain in ACMI, establishing clear ownership and accountability at every stage.

## Core Principles

1. **One handoff event per completion** — When an agent finishes their stage, they log exactly one `handoff-complete` event.
2. **Acknowledge before acting** — The receiving agent must acknowledge (`handoff-ack`) before beginning work.
3. **Correlation chains connect the flow** — Every handoff links back through `correlationId` and `parentCorrelationId` to form a complete audit trail.
4. **Signal state reflects current stage** — Agents update their ACMI signals to show their current status and work item.
5. **Quality gates gate the handoff** — The receiving agent checks quality criteria before accepting.

## Handoff Event Schema

### Sender (completing work)

```typescript
acmi_event(
  namespace: "work",              // Always use work namespace for pipeline handoffs
  id: "<work-item-id>",          // The specific work item being handed off
  source: "agent:<sender-id>",   // Who completed the work
  kind: "handoff-complete",      // Fixed kind for stage completion
  correlationId: "<senderId>HandoffTo<receiverId>-<epochMs>",
  summary: "[handoff-complete @<receiver-id>] <work-item-title> — <summary-of-work-done>"
)
```

### Receiver (acknowledging)

```typescript
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:<receiver-id>",
  kind: "handoff-ack",
  parentCorrelationId: "<senderCorrelationId>",  // Links back to sender's handoff
  correlationId: "<receiverId>Ack<handoffPrefix>-<epochMs>",
  summary: "[handoff-ack] Picking up <work-item-title> at <stage-name> stage"
)
```

## Handoff Sequence

### Sequential Handoffs

For stages with a single owner, handoffs are straightforward:

```
Agent A (completes)
  → handoff-complete (kind: "handoff-complete", addressed to Agent B)
  → signals: status="idle"
  
Agent B (receives)
  → acmi_bootstrap to get context
  → Reads handoff event from timeline
  → handoff-ack (kind: "handoff-ack", parentCorrelationId back to A)
  → signals: status="working", current_work_item="..."
  → Begins work
```

### Parallel Handoff (Review Stage)

The Review stage is special — 3 agents work in parallel. The handoff flow:

```
UI Designer (completes Design stage)
  → handoff-complete addressed to all 3 reviewers
  → [@design-brand-guardian, design-visual-storyteller, design-inclusive-visuals-specialist]

Reviewers (each independently):
  → handoff-ack → begins review → review-pass OR review-fail

After all 3 pass:
  → Orchestrator detects all review-pass events
  → Handoff to Whimsy Injector
```

#### Parallel Handoff Completion Detection

The orchestrator monitors the work item timeline. When all 3 reviewers have logged `review-pass`, the stage is considered complete. Use `acmi_cat` to view the consolidated timeline:

```typescript
acmi_cat(
  keys: ["work:<work-item-id>:timeline"],
  since: "since-last-handoff-timestamp"
)
```

Count `review-pass` events — when count >= 3, all reviewers have approved.

## Handback Protocol (Quality Gate Failure)

When a review fails, the work is sent back to the originating stage.

### Handback Event

```typescript
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:<reviewer-id>",
  kind: "handback",
  correlationId: "<reviewerId>HandbackTo<originatingAgent>-<epochMs>",
  parentCorrelationId: "<originalHandoffCorrelationId>",
  summary: "[handback @<originating-agent>] <work-item-title> — issues: <comma-separated-issues>"
)

// Also log a review-fail with details
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "agent:<reviewer-id>",
  kind: "review-fail",
  correlationId: "<reviewerId>ReviewFail-<epochMs>",
  summary: "[review-fail] <work-item-title> — <detailed-issues>"
)
```

### Rework Cycle

1. The originating agent receives the handback
2. They address the issues
3. They re-submit via a new `handoff-complete` event
4. The reviewer re-evaluates
5. Maximum 3 rework cycles before escalation

### Escalation

If a work item exceeds 3 rework cycles, the orchestrator creates an escalation event:

```typescript
acmi_event(
  namespace: "work",
  id: "<work-item-id>",
  source: "system:orchestrator",
  kind: "coord-note",
  correlationId: "<workItemId>Escalation-<epochMs>",
  summary: "[coord-note @stakeholder] <work-item-title> exceeded rework limit — escalation required"
)
```

## Complete Handoff Chain Reference

```
Stage                    Sender                          Receiver(s)                         Event Kind
──────────────────────────────────────────────────────────────────────────────────────────────────────────
Backlog → Research       orchestrator                    design-ux-researcher                handoff-complete
Research → Architecture  design-ux-researcher            design-ux-architect                 handoff-complete
Architecture → Design    design-ux-architect             design-ui-designer                  handoff-complete
Design → Review          design-ui-designer              design-brand-guardian               handoff-complete
                                                         design-visual-storyteller
                                                         design-inclusive-visuals-specialist
Review → Delight         orchestrator (after 3 passes)   design-whimsy-injector              handoff-complete
Delight → Assets         design-whimsy-injector          design-image-prompt-engineer         handoff-complete
Assets → Done            design-image-prompt-engineer    orchestrator                        handoff-complete
```

## Signal Updates During Handoff

Agents MUST update their ACMI signals at the following points:

### Before Starting Work
```typescript
acmi_signal(namespace: "agent", id: "<agent-id>", signals: JSON.stringify({
  status: "working",
  current_work_item: "<work-item-id>",
  current_stage: "<stage-name>",
  started_at: "<iso-timestamp>",
  progress_pct: 0
}))
```

### During Work (Progress Updates)
```typescript
acmi_signal(namespace: "agent", id: "<agent-id>", signals: JSON.stringify({
  progress_pct: <0-100>,
  last_activity: "<brief-update>"
}))
```

### After Completion (Returning to Idle)
```typescript
acmi_signal(namespace: "agent", id: "<agent-id>", signals: JSON.stringify({
  status: "idle",
  current_work_item: null,
  current_stage: null,
  last_completed: "<work-item-id>",
  last_completed_at: "<iso-timestamp>"
}))
```

## Thread Coordination

For complex handoffs requiring discussion, agents use ACMI threads:

```typescript
acmi_event(
  namespace: "thread",
  id: "design-agency-<work-item-id>",
  source: "agent:<agent-id>",
  kind: "coord-note",
  correlationId: "<agentId>CoordNote-<epochMs>",
  summary: "[coord-note] <work-item-title> — <question-or-update>"
)
```

## Error Handling

### Agent Not Responding
If a receiving agent doesn't acknowledge within a reasonable timeframe:
1. Orchestrator checks the agent's signals for status
2. If signals show "working" — agent is busy, add to queue
3. If signals show "idle" — resend handoff
4. If no response after 3 retries, log escalation

### Lost Handoff Detection
To find orphaned work items (handoffs that were sent but never acknowledged):
```typescript
acmi_cat(
  keys: ["work:<work-item-id>:timeline"],
  since: "1h"  // or appropriate window
)
// Look for handoff-complete without matching handoff-ack
```
