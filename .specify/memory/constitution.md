<!--
Sync Impact Report
Version change: none → 1.0.0
Modified principles:
- Placeholder Principle 1 → MCP-Strict Interfaces
- Placeholder Principle 2 → FastRender Swarm Discipline
- Placeholder Principle 3 → HITL Confidence Governance
- Placeholder Principle 4 → Agentic Commerce Safeguards
- Placeholder Principle 5 → Spec-First Evidence & Observability
Added sections:
- Additional Constraints: Data Fabric & Security Controls
- Development Workflow & Quality Gates
Removed sections: none
Templates requiring updates (✅ updated / ⚠ pending):
- ✅ .specify/templates/spec-template.md – aligns with constitution (no change required)
- ✅ .specify/templates/plan-template.md – Constitution Check enforces these principles (no change required)
- ✅ .specify/templates/tasks-template.md – Guidance already reflects story-first, testable tasks (no change required)
Follow-up TODOs: none
-->

# Project Chimera Constitution

## Core Principles

### I. MCP-Strict Interfaces (NON-NEGOTIABLE)
Every external integration MUST be exposed through a contract-tested MCP server before agents can call it. No Planner, Worker, or Judge may perform direct API calls, database access, or filesystem reads outside the MCP host runtime. Each MCP server requires schemas, rate-limit policies, and audit logging so that failures or API churn stay isolated at the edge. Breaking this rule halts deployment.

### II. FastRender Swarm Discipline
Planner, Worker, and Judge services operate as independently deployable units that only communicate via the task DAG and review queues described in the SRS. Planners own goal decomposition, Workers execute single atomic tasks, and Judges gate all state mutations using optimistic concurrency. Any new capability must document how it respects this hierarchy and include replayable traces for post-mortems.

### III. HITL Confidence Governance
No artifact reaches a public surface until a Judge stamps it with a confidence score and routes it according to the 0.90/0.70 thresholds. Sensitive-topic filters override confidence and force human review. Feature work MUST define how outputs are scored, how evidence for the score is persisted, and how humans can override or annotate outcomes.

### IV. Agentic Commerce Safeguards
Wallet actions run through the CFO Judge, enforce governor limits (spend, volume, counterparties), and emit immutable ledger events. Any code touching finances must provide dry-run capability, budget checks, and anomaly detection hooks. Keys stay in managed secret stores; no plaintext secrets may appear in repos, logs, or telemetry.

### V. Spec-First Evidence & Observability
Specs are the single source of truth. Every feature delivers measurable outcomes, test artifacts, and structured logging that ties Planner decisions to Worker outputs and Judge rulings. Contract tests precede implementation, GitHub Actions enforce lint/test gates, and documentation (SOUL.md, schemas, task definitions) updates alongside code.

## Additional Constraints: Data Fabric & Security Controls
PostgreSQL + pgvector hold authoritative transactional and embedding state; Redis covers ephemeral coordination; Weaviate stores long-term semantic memory. Schema migrations MUST precede runtime changes and include rollbacks. Persona data in SOUL.md is version-controlled, and memory writes must cite provenance to prevent drift. All secrets rely on managed stores, and OpenClaw-style supply-chain risks require signed skill bundles plus automated CVE scanning before promotion.

## Development Workflow & Quality Gates
Every initiative begins with `/speckit.specify` to capture user-value slices, followed by `/speckit.plan` to document constitution gates, architecture choices, and project structure. `/speckit.tasks` maps plan outputs into independently testable story tracks. Implementation cannot start until the Constitution Check in plan.md confirms MCP compliance, HITL routing, and budget controls. Code reviews verify logs, tests, and contract artifacts; deployments require successful CI plus documented HITL playbooks.

## Governance
This constitution supersedes team preferences. Amendments require an RFC referencing affected specs, updated gates in plan/tasks templates, and sign-off from the Super-Orchestrator role. Semantic versioning applies: MAJOR for principle rewrites or removals, MINOR for new principles/sections, PATCH for clarifications. Compliance reviews happen at each release; failing a principle blocks merge until remedied. Runtime guidance in research/ and specs/ must cite the relevant principle IDs for traceability.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
