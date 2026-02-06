# Implementation Plan: Chimera Autonomous Trend Analysis Agent

**Branch**: `001-chimera-agent-blueprint` | **Date**: 2026-02-06 | **Spec**: [specs/001-chimera-agent-blueprint/spec.md](specs/001-chimera-agent-blueprint/spec.md)
**Input**: Feature specification from `/specs/001-chimera-agent-blueprint/spec.md`

## Summary
Build a Planner→Worker→Judge feature slice that (1) scores MCP trend resources and spawns DAG tasks, (2) produces persona-locked multi-modal artifacts with budget telemetry, and (3) exposes signed availability/status broadcasts to the OpenClaw network so external swarms can coordinate with Chimera agents. The implementation relies on Python-based services (CrewAI/LangGraph orchestration) backed by PostgreSQL + pgvector, Redis task queues, Weaviate memories, and a dedicated `mcp-server-openclaw` for publishing status beacons.

## Technical Context

**Language/Version**: Python 3.11 for services, TypeScript (React) for HITL console (unchanged).  
**Primary Dependencies**: CrewAI (current orchestrator), LangGraph parity mode, FastAPI for internal APIs, SQLAlchemy, Redis-py, Weaviate client, Coinbase AgentKit, MCP Python SDK, Pydantic, pytest.  
**Storage**: PostgreSQL 16 + pgvector for tasks/agents/artifacts; Redis for task/review queues and spend counters; Weaviate for semantic memory; blockchain ledger via AgentKit for wallet reconciliation.  
**Testing**: pytest + coverage for services, contract tests for MCP servers (schemathesis/newman), data-migration tests via pytest + pg fixtures, end-to-end swarm replay tests using synthetic MCP resources.  
**Target Platform**: Linux/Kubernetes cluster (containers) with CI/CD via GitHub Actions.  
**Project Type**: Multi-service backend (planner, worker, judge, MCP servers) with shared library packages under `src/chimera`.  
**Performance Goals**: Detect → task creation ≤5s p95; Worker+Judge latency <10s median excluding HITL; OpenClaw status ACK <60s; trend throughput ≥1k signals/hr.  
**Constraints**: MCP-only integrations, Judge confidence routing (≥0.90 auto, 0.70–0.90 HITL, <0.70 reject), budget governors ($50 daily default), sensitive-topic override, signed skill bundles, OCC for state writes.  
**Scale/Scope**: Target 1k concurrent agents in swarm, each publishing status every ≤60s when active; multi-tenant support for at least 5 campaigns.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance Plan |
| --- | --- |
| MCP-Strict Interfaces | All new external touch points (trend feeds, OpenClaw status, Coinbase AgentKit) run through MCP servers with contract tests; no direct API calls from Planner/Worker/Judge. |
| FastRender Swarm Discipline | Planner service owns resource polling + DAG creation, Workers remain stateless executors, Judges gate commits + OCC, with queue-based messaging and trace IDs. |
| HITL Confidence Governance | Confidence scores computed per artifact; routing thresholds enforced server-side; HITL UI enhancements prioritized in quickstart; sensitive-topic filters override automation. |
| Agentic Commerce Safeguards | CFO Judge validates OpenClaw collaboration requests and any downstream wallet actions; Redis spend counters + budget decorators enforced; ledger persisted in `wallet_ledger`. |
| Spec-First Evidence & Observability | This plan + research/data-model/contracts produced before code; telemetry (trace_id, confidence, costs) logged; GitHub Actions gating tests/migrations. |

Result: **PASS** – requirements aligned with Constitution v1.0.0. Any deviation must be justified via RFC before implementation.

## Project Structure

### Documentation (this feature)

```text
specs/001-chimera-agent-blueprint/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openclaw-status.json
└── tasks.md (generated later via /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── chimera/
│   ├── planner/               # Trend ingestion + DAG creation
│   ├── worker/                # Multi-modal content executors
│   ├── judge/                 # Confidence gating + HITL routing
│   ├── skills/
│   │   └── openclaw/          # MCP server + availability publisher
│   ├── shared/
│   │   ├── contracts/         # Pydantic models for Planner↔Worker↔Judge
│   │   └── telemetry/         # Trace/log utilities
│   └── cli/                   # Maintenance scripts (e.g., replay trend feeds)
tests/
├── unit/
│   ├── planner/
│   ├── worker/
│   └── judge/
├── integration/
│   ├── swarm/                 # Planner→Worker→Judge replay tests
│   └── openclaw/
└── contract/
    └── mcp_servers/          # JSON schema + status publisher validation
```

**Structure Decision**: Maintain a single `src/chimera` package with service-specific submodules plus shared contracts to preserve theme-level reuse while keeping FastRender roles separated. Tests mirror runtime layout (unit/integration/contract). MCP server lives under `skills/openclaw` for parity with other runtime skills.

## Complexity Tracking

No Constitution violations identified; table intentionally left empty.
