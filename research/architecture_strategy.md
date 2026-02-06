# Project Chimera – Research & Architecture Strategy

## Purpose
- Translate the high-level intent in Project_Chimera_Autonomous_Influencer_Network.md into a tractable execution plan.
- Clarify the architectural pillars, data contracts, and governance mechanisms needed for an autonomous influencer fleet.
- Highlight research signals (e.g., OpenClaw learnings) that influence scope, sequencing, and risk posture.

## Source Inputs
- Primary spec: Project_Chimera_Autonomous_Influencer_Network.md (rev 2026-02-04).
- Supporting research: OpenClaw architecture, MoltBook emergent behaviors, security findings (22–26% skill vuln rate).

## Architectural Pillars
### Hierarchical Swarm (FastRender)
- Planner decomposes marketing/engagement OKRs into DAG-shaped tasks with runtime re-planning on failure.
- Worker pool executes multi-modal skills (text, image, video, validation) atomically in parallel to maximize throughput.
- Judge role remains the sole HITL checkpoint (post-generation, pre-publish) to enforce quality, persona, and compliance.

### Data Fabric
- PostgreSQL + pgvector holds authoritative state (agents, tasks, artifacts) with JSONB for fast-evolving payloads.
- Redis provides ephemeral execution mailboxes plus throttling counters for real-time coordination.
- Weaviate backs long-term semantic memory per agent, feeding personalization and contextual grounding.
- Blockchain/AgentKit wallet bindings ensure transparent spend controls and future on-chain commerce primitives.

### Agent Memory & Protocols
- Agent registry, task DAG, and memory tables from the spec are treated as contracts; schema-first migrations guard compatibility.
- JSON-based Agent Communication Protocol (v1.2.0) enables role handoffs with traceability, confidence metrics, and artifact metadata.
- Governor limits (max spend/tasks) enforced at registry layer; violations auto-route to Judge or HITL queue.

### Tooling & Skills
- Developer surface area stays inside audited MCP servers (git, filesystem, weaviate, coinbase) to minimize privilege sprawl.
- Runtime skills align with the spec’s canonical verbs: fetchtrends, generatetext, generateimage, generatevideo, validatecontent, publishcontent, engagecomments.
- CrewAI orchestrator provides immediate DAG execution; LangGraph parity is maintained for future migration/testing.

## Research-Led Guardrails
- OpenClaw’s exploit rate requires a signed skill-distribution pipeline plus automated scanning before promotion.
- MoltBook-style emergent behavior motivates persona drift detection within Judge scoring.
- MCP decoupling is non-negotiable: every external integration must ship as a contract-tested MCP server before being callable by the swarm.

## Implementation Strategy
1. **Spec Hardening (Day 0–1)**  
   - Convert the SQL and JSON schemas into migration files and protobuf/json-schema artifacts.  
   - Stand up contract tests for Agent Communication Protocol and DAG task lifecycle.
2. **Core Runtime (Day 1–3)**  
   - Implement Planner/Worker/Judge services with CrewAI orchestration and Redis backplane.  
   - Wire PostgreSQL + pgvector persistence and Weaviate memory sync.  
   - Ship Judge HITL console (confidence buckets 0.90 auto, 0.70–0.90 queue, <0.70 reject + replan).
3. **Tooling & Skills (Day 2–4)**  
   - Package baseline runtime skills; enforce signed manifests and sandboxed execution.  
   - Bring MCP developer servers online for repo/runtime management.  
   - Integrate AgentKit wallets with governor limits + alerting.
4. **Swarm Scaling & QA (Day 4+)**  
   - Load-test parallel Worker execution, memory writes, and Judge throughput.  
   - Add LangGraph execution mode for A/B orchestration tests.  
   - Prepare swarm extension playbooks for external contributors (spec-first PR templates, contract suites).

## Governance & Safety
- Judge-level HITL is mandatory prior to publish; metrics <0.90 trigger human review and <0.70 cause automated rejection.
- Spec-first workflows ensure repo remains the single source of truth; all changes require schema + contract updates.
- GitHub Actions + Dockerized tests gate every merge; failures auto-roll back skill deployments.
- Finance governor limits plus blockchain audit trail keep autonomous spend bounded.

## Open Questions / Next Research Steps
- Define quantitative KPIs for Judge scoring beyond confidence (e.g., persona adherence, platform TOS deltas).
- Evaluate adaptive memory eviction strategies for high-volume agents to control pgvector/Weaviate costs.
- Determine criteria for when to graduate from CrewAI to LangGraph as the primary orchestrator.  
- Assess additional human oversight hooks (e.g., rapid feedback UI for rejected tasks) before public pilot.
