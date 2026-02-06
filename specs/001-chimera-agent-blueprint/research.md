# Research – Chimera Autonomous Trend Analysis Agent

## Decision 1: Trend Signal Processing Pipeline
- **Decision**: Use a dedicated Planner telemetry service that polls MCP resources, applies a lightweight LLM-based semantic filter (Gemini 3 Flash) to score relevance, and enqueues `trend_analysis` tasks with OCC state versions.
- **Rationale**: Keeps FastRender Planner stateless, enables deterministic replays, and aligns with resource/trace patterns already defined in the SRS.
- **Alternatives Considered**:
  - Passive pull triggered by Operators → rejected (manual overhead, violates autonomy goal).
  - Worker-driven polling → rejected (breaks Planner/Worker separation, complicates OCC).

## Decision 2: OpenClaw Availability Broadcast
- **Decision**: Ship a standalone `mcp-server-openclaw` exposing `status.publish_availability`, `status.revoke`, and `status.fetch_neighbors` that signs payloads with AgentKit keys and logs acknowledgements in PostgreSQL.
- **Rationale**: Preserves MCP-only rule, isolates OpenClaw-specific logic, and enables contract testing + rate limiting independent of core swarm code.
- **Alternatives Considered**:
  - Embedding OpenClaw calls directly in Planner → rejected (violates MCP-Strict Interfaces, harder to rotate keys).
  - Using MoltBook relay without signatures → rejected (high spoofing risk per OpenClaw research).

## Decision 3: Judge Confidence & HITL Evidence
- **Decision**: Extend Judge service to persist reasoning traces, persona adherence scores, and cost telemetry with each decision, feeding HITL UI and enabling automated escalation when queue depth >50.
- **Rationale**: Required by constitution principle III, provides Operators with context to make rapid approvals, and supports future analytics.
- **Alternatives Considered**:
  - Simple boolean approvals without traces → rejected (insufficient observability, no audit trail).
  - Pushing evidence only to logs → rejected (hard to expose in HITL UI, no structured queries).

## Decision 4: Budget Governance for OpenClaw Intents
- **Decision**: Pre-check every OpenClaw collaboration intent using Redis-backed spend counters + CFO Judge policies before Planner accepts tasks.
- **Rationale**: Ensures Agentic Commerce safeguards apply even when work originates externally; prevents resource exhaustion.
- **Alternatives Considered**:
  - Accept all intents then throttle in Worker stage → rejected (wastes DAG capacity, could exceed budgets before CFO review).
  - Manual Operator approval for each intent → rejected (breaks autonomy, increases latency).
