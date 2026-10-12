---
name: web4-skill
description: Use this skill when building, designing, or styling Web4 decentralized AI agent interfaces, spatial canvas controls, cryptographic contract widgets, agent-to-agent communication HUD overlays, decentralized identity (DID) badges, and real-time ACMI telemetry streams in OpenDesign 0.7.0.
license: Apache-2.0
---

# Web4 Decentralized AI Agent Design System & Skill

The **Web4 Design Standard** specifies UI/UX primitives for next-generation decentralized agentic applications. Web4 bridges spatial web interfaces, autonomous multi-agent coordination, cryptographic wallet/smart contract widgets, and real-time agent memory streams (ACMI).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       WEB4 SPATIAL AGENT INTERFACE                          │
│                                                                             │
│ ┌─────────────────────────┐ ┌──────────────────────┐ ┌────────────────────┐ │
│ │  Decentralized ID (DID) │ │  Agent-to-Agent HUD  │ │ ACMI Telemetry ZSET│ │
│ │  Wallet / Identity     │ │  Spatial Canvas      │ │ Real-Time Stream   │ │
│ └─────────────────────────┘ └──────────────────────┘ └────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1. Core Principles

- **Agent-First Navigation**: Layouts prioritize machine-to-machine telemetry alongside human supervisory controls.
- **Translucent Obsidian Glass**: Deep void black (`#0B0C10`) paired with frosted charcoal glass panels (`rgba(18, 20, 29, 0.70)`) and electric blue (`#1856FF`) / cyber cyan (`#00F0FF`) telemetry highlights.
- **Cryptographic & ACMI Verification**: Every interactive widget includes cryptographic origin badges, transaction hash previews, and ACMI `correlationId` chain references.

## 2. Key Component Primitives

### A. Agent-to-Agent Spatial HUD Overlay
```html
<div class="web4-hud-panel madez-glass-card">
  <div class="web4-agent-badge">
    <span class="web4-status-dot online"></span>
    <span class="web4-did">did:key:z6MkpTHR...</span>
    <span class="madez-badge-cyan">ACMI v1.5</span>
  </div>
  <div class="web4-stream-feed">
    <div class="web4-event-node">
      <span class="kind">coord-note</span>
      <span class="cid">web4Contract-1785170700000</span>
    </div>
  </div>
</div>
```

### B. Smart Contract Execution Widget
```html
<div class="web4-contract-card">
  <div class="web4-contract-header">
    <h3>Decentralized Escrow Contract</h3>
    <span class="web4-network-pill">Base Mainnet</span>
  </div>
  <div class="web4-contract-state">
    <div class="metric">
      <label>Stake</label>
      <value>2.5 ETH</value>
    </div>
    <div class="metric">
      <label>Agent Quorum</label>
      <value>3 / 4 Signed</value>
    </div>
  </div>
</div>
```

## 3. CSS Token Reference
```css
:root {
  --web4-bg: #0B0C10;
  --web4-surface-glass: rgba(18, 20, 29, 0.75);
  --web4-accent-blue: #1856FF;
  --web4-accent-cyan: #00F0FF;
  --web4-accent-gold: #F5EBE0;
  --web4-border-glass: rgba(255, 255, 255, 0.10);
  --web4-font-mono: 'JetBrains Mono', monospace;
}
```

## 4. Anti-Patterns
- Do NOT use opaque light gray cards or static non-responsive table layouts.
- Do NOT omit correlationId chains or cryptographic status indicators on interactive cards.
- Do NOT break the purple ban rule (no violet/purple primary themes).
