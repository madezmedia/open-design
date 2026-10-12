# ACMI Protocol Specification — v1.4 (aligned)

This is a condensed working reference for skill use, fully aligned with **ACMI v1.4**, **Comms v1.1 event schema**, and **Protocol 9 (Git Atomic Git Sync)**.

## The three slots

Every entity has exactly three slots:

| Slot | Question | Storage | Mutation |
|---|---|---|---|
| `profile` | who | JSON document | overwrite + shallow merge |
| `signals` | now | KV map of JSON values | per-key set / delete |
| `timeline` | then | sorted set of events | append-only |

That's the entire data model. No other shapes, no other operations.

## Entity IDs

`<category>:<id>` — combined ≤ 256 chars.
- `<category>` matches `[a-z][a-z0-9_-]*`
- `<id>` matches `[a-zA-Z0-9_.-]+`

Adapter-side keys: `acmi:<category>:<id>:<slot>`. Reserved prefixes: don't use `acmi:` in your own IDs.

## Profile slot — operations

- `profileGet(id) → ProfileDoc | null`
- `profileSet(id, doc)` — overwrite
- `profileMerge(id, partial)` — shallow merge (top-level only)
- `profileDelete(id)`

Reads return copies; mutating the returned object MUST NOT affect storage.

## Signals slot — operations

- `signalsGet(id, key) → value | undefined`
- `signalsSet(id, key, value)`
- `signalsAll(id) → Record<string, value>`
- `signalsDelete(id, key)`

Storage may be STRING+JSON or native HASH; the choice is invisible to callers.

## Timeline slot — operations + Comms v1.1 event schema

- `timelineAppend(id, event)`
- `timelineRead(id, opts?) → events[]`
- `timelineSize(id) → number`

Every event MUST adhere strictly to the **Comms v1.1 event schema**. The following five core fields are required:

| Field | Type | Notes |
|---|---|---|
| `ts` | number | Wall-clock ms; monotonicity not required across writers |
| `source` | string | Entity-ID-formatted: `agent:foo`, `user:mikey` |
| `kind` | string | Event taxonomy |
| `correlationId` | string | Chain identifier (descriptive camelCase + ms epoch) |
| `summary` | string | Human-readable, ≤500 chars (with `[kind-tag @recipient]` convention) |

### Optional & Extended Fields
- `parentCorrelationId`: string (required for chaining)
- `payload`: JSON object (custom metadata)
- `tags`: string[] (for indexing)
- `speaker_type`: string (v1.3 OPTIONAL → **v1.4 REQUIRED** for agent vs. human verification)

`timelineRead` options: `limit`, `reverse`, `sinceMs`, `untilMs`.

**Append-only.** No mutation/deletion in the protocol; adapters MAY support it for compliance.

---

## v1.4 additions & Alignments

### 1. Verification with `speaker_type`
To distinguish synthesizable agent reasoning from lived-experience human input, `speaker_type` is now **REQUIRED** on all timeline events:
- `"agent"`: Spawned or scheduled LLM/scripted processes
- `"human"`: Direct user-typed input

### 2. Multi-actor (§11)
Profiles MUST declare `actor_type ∈ {agent, human, system, external}`.

| `actor_type` | Primary key prefix | Notes |
|---|---|---|
| `agent` | `acmi:agent:<id>:*` | Autonomous LLM/scripted |
| `human` | `acmi:user:<id>:*` | Note: `user:` prefix, not `human:` |
| `system` | (no profile required) | Cron, webhooks, telemetry |
| `external` | `acmi:external:<id>:*` | Clients, vendors |

**Dual-projection forbidden.** Same `<id>` cannot exist in both `agent:` and `user:`. Resolve via §11.5 deprecation procedure.

### 3. Multi-tenant (§12)
Optional `tenant_id` on profiles:
- `"madez"` (default)
- `"client:<slug>"` per-client
- `"shared"` cross-tenant entities (registries, protocol data)

Workspace sub-scope (within a tenant) keeps the older `acmi:workspace:<workspace>:*` form.

---

## Protocol 9 — Git Atomic Git Protocol

Protocol 9 governs the coordination of multi-agent and human developer git operations, enforcing atomic branch locks, single-purpose commits, and ACMI-bus synchronization.

### The Lifecycle
1. **Branch Lock (§7 Lock-Protocol):** Acquire branch lock on `thread:git-sync` by setting the signal key `locked_by` to the agent's ID to prevent split-brain conflicts.
2. **Atomic Modification:** Perform a single, highly focused, cohesive code change.
3. **Atomic Commit:** Create a git commit with a message including the active ACMI `correlationId` in the body.
4. **Pushed Notification:** Append an event of `kind: git-commit-pushed` to the `thread:git-sync` timeline with the commit hash and branch.
5. **Release Lock:** Clear the branch lock signals. Other fleet agents pull changes incrementally before continuing their tasks.
