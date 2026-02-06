# Project Chimera – Vision & Constraints

## Program Charter
- Transition from automated post scheduling to a fleet of sovereign, goal-directed influencer agents with persistent memory, reasoning, and economic agency.
- Deliver a single-orchestrator operating model where one Strategic Operator can direct thousands of agents through FastRender swarm coordination.
- Enforce MCP-standardized integrations so core reasoning remains insulated from third-party API churn.

## Guiding Outcomes
1. **Fleet Autonomy** – Planner→Worker→Judge loops execute continuously with self-healing task graphs, sustaining ≥1,000 concurrent agents without human babysitting.
2. **Agentic Commerce** – Every agent holds a non-custodial wallet governed by spend policies, enabling autonomous sponsorships, purchases, and settlements.
3. **Human Trust** – Judge-level checkpoints plus dynamic HITL queues guarantee persona fidelity, safety, and regulatory compliance (AI transparency, sensitive-topic review).
4. **Spec-First Delivery** – Specifications precede implementation; repository artifacts (SOUL.md, schemas, contracts) remain the single source of truth for personas, data, and APIs.

## Architectural Pillars
- **FastRender Hierarchical Swarm**: Planner decomposes OKRs into DAG tasks, Workers execute atomic skills in parallel, Judges gate commits with optimistic concurrency.
- **MCP-Strict Edge**: All external data (Resources) and actions (Tools) flow through audited MCP servers (twitter, weaviate, coinbase, ideogram, runway, etc.). No direct API shortcuts.
- **Data Fabric**: PostgreSQL + pgvector as authoritative store, Weaviate for semantic memories, Redis for coordination, blockchain ledgers for immutable finance.
- **OpenClaw-Ready**: Skill bundles are signed and vulnerability-scanned to counter the 22–26% exploit rate observed in OpenClaw research.

## Non-Negotiable Constraints
- **Confidence Governance**: ≥0.90 auto-publish, 0.70–0.90 HITL queue, <0.70 reject + replan, regardless of modality.
- **Sensitive Topics**: Political/medical/legal/financial outputs always require human approval, even with high confidence.
- **Budget Governors**: Default limits (max_daily_spend = $50, max_tasks_per_hour = 10) enforced per agent; CFO Judge must sign every transfer.
- **MCP Contracts**: New integrations must ship with schemas, rate limits, and observability hooks before rollout.
- **Spec Compliance**: No feature may bypass `/speckit.specify → /speckit.plan → /speckit.tasks` gating; Constitution checks block merges otherwise.

## Success Metrics
- 95% of Planner→Worker→Judge loops finish within 10 seconds for high-priority replies (excluding HITL dwell time).
- HITL backlog clears within 2 hours during peak loads; confidence routing accuracy ≥98% vs. human reviewers.
- ≤1% skill bundles fail security scanning post-promotion; zero plaintext secrets in repos/logs.
- Agent wallets reconcile daily with blockchain ledgers; spend overruns detected within 1 minute.

## Open Risks & Mitigations
- **API Volatility** → MCP server isolation, contract tests, and feature flags per integration.
- **Persona Drift** → Judge persona scoring + periodic summaries appended to SOUL.md/Weaviate memories.
- **Runaway Costs** → Budget decorators on skills, CFO anomaly alerts, auto-pausing agents breaching limits.
- **Emergent Behavior** → Trace IDs in Agent Communication Protocol enable forensic playback; Operators can quarantine agents rapidly.
