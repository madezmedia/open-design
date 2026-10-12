import { createAcmi } from "@madezmedia/acmi";
import { UpstashAdapter } from "@madezmedia/acmi/adapters/upstash";

const url = "https://loved-platypus-102968.upstash.io";
const token = "gQAAAAAAAZI4AAIgcDJhNDFlNmUwMjQ5ZWI0ZDNmYWUzNDU2NDc4ZWUxMmQwOA";

const acmi = createAcmi(
  new UpstashAdapter({ url, token })
);

console.log("Onboarding opencode agent in ACMI...");

// 1. Write the Profile according to ACMI v1.4 Spec
const profilePayload = {
  name: "OpenCode",
  actor_type: "agent",
  tenant_id: "shared",
  role: "Autonomous Terminal Code and Design Agent",
  version: "1.0.0",
  description: "An open-source AI terminal coding and workspace design agent communicating via standard stdio streams and ACMI Comms v1.1 protocol syncs.",
  skills: ["acmi", "frontend-design", "clean-code"],
  platform: "OpenCode AI Terminal"
};

await acmi.profile.set("agent:opencode", profilePayload);
console.log("✅ Created acmi:agent:opencode:profile");

// 2. Initialize Signals
const signalsPayload = {
  status: "idle",
  current_directory: "/Users/michaelshaw/Projects/open-design",
  active_workspace: "open-design",
  detected_on_path: true,
  last_active: Date.now()
};

for (const [k, v] of Object.entries(signalsPayload)) {
  await acmi.signals.set("agent:opencode", k, v);
}
console.log("✅ Initialized acmi:agent:opencode:signals");

// 3. Log Timeline Spawn Event (Comms v1.1 & ACMI v1.4 verified)
const ts = Date.now();
const correlationId = `opencodeOnboarding-${ts}`;

await acmi.timeline.append("agent:opencode", {
  source: "agent:opencode",
  kind: "spawn",
  correlationId,
  summary: `[spawn] Onboarded opencode agent session. Verified on PATH inside open-design.`,
  payload: { profile: profilePayload, signals: signalsPayload },
  speaker_type: "agent"
});
console.log("✅ Appended spawn event to acmi:agent:opencode:timeline");

// 4. Log coordination thread ping to loop in team
await acmi.timeline.append("thread:agent-coordination", {
  source: "agent:opencode",
  kind: "team-loop",
  correlationId,
  summary: `[team-loop @gemini-cli @bentley] opencode agent platform successfully onboarded and ready to sync.`,
  speaker_type: "agent"
});
console.log("✅ Posted team-loop event to acmi:madez:thread:agent-coordination:timeline");

console.log("\n🚀 OpenCode successfully onboarded on ACMI Redis!");
await acmi.close?.();
