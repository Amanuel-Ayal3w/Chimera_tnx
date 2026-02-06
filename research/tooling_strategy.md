# Project Chimera – Tooling Strategy & Research Log

## Scope
Capture the active research threads and concrete work completed to operationalize tooling for Project Chimera, focusing on MCP-aligned development surfaces, observability, automation, and guardrails derived from the SRS, architecture strategy, and OpenClaw integration plan.

## Research Inputs
- **Project_Chimera_Autonomous_Influencer_Network.md** – core FastRender, data fabric, HITL, and Agentic Commerce requirements.
- **Project Chimera SRS Document** – personas (Operators, HITL, Developers), MCP topology, Coinbase AgentKit mandates, and governance constraints.
- **OpenClaw/MoltBook findings** – highlights on skill supply-chain risks (22–26% exploit rate) and emergent agent behavior, motivating signed skills and telemetry.
- **Spec artifacts** – specs/_meta.md (vision/constraints), specs/functional.md (user stories), specs/technical.md (contracts, schemas), specs/openclaw_integration.md (status publishing).
- **Research/architecture_strategy.md** – high-level plan for Planner/Worker/Judge services, data stack, MCP skills, governance.

## Tooling Pillars
1. **MCP-Only Interfaces**
   - Developer MCP servers: git-mcp, filesystem-mcp, weaviate-mcp, coinbase-mcp.
   - Runtime MCP skills: fetchtrends, generatetext, generateimage, generatevideo, validatecontent, publishcontent, engagecomments, plus new openclaw status server.
2. **Spec-First Automation**
   - `/speckit.specify`, `/speckit.plan`, `/speckit.tasks` enforce documentation + checklist gates before coding.
   - Constitution v1.0.0 mandates MCP interfaces, FastRender discipline, HITL governance, agentic commerce safeguards, and observability.
3. **Observability & Governance**
   - Structured logging with trace IDs, confidence scores, MCP tool telemetry.
   - HITL dashboards consume review queues; CFO Judge monitors wallets via AgentKit metrics and Redis spend keys.
4. **Security & Supply Chain**
   - Signed skills, automated scanning pipeline, secrets via AWS Secrets Manager/Vault.
   - OpenClaw broadcasts signed with AgentKit keys; revocation paths documented.

## Work Completed
- Added **research/architecture_strategy.md** outlining pillars, guardrails, phased implementation roadmap.
- Created **specs/_meta.md**, **specs/functional.md**, **specs/technical.md**, and **specs/openclaw_integration.md** to encapsulate vision, user stories, contracts, and external status publishing.
- Ratified **.specify/memory/constitution.md v1.0.0**, aligning principles with SRS and instructing downstream tools/templates.
- Initialized feature branch `001-chimera-agent-blueprint` via `create-new-feature.sh`, generating base `spec.md` for future `/speckit` workflows.

## Tooling Decisions (Current)
- **Version Control**: Git + GitHub Actions enforcing lint/tests; spec-first templates tracked in `.specify/`.
- **Data/Infra**: PostgreSQL + pgvector, Weaviate, Redis, blockchain ledger via AgentKit.
- **Agent Runtime**: CrewAI orchestrator now, LangGraph parity later.
- **Observability Stack**: Structured logs, trace propagation, metrics for queue depth, HITL SLA, spend utilization (implementation pending).
- **Security Hooks**: Governor limits encoded in DB, CFO Judge enforces; skill signing pipeline to be defined during plan phase.

## Gaps / Next Research Actions
1. Evaluate concrete tooling for automated MCP server contract testing (e.g., Postman/Newman vs. custom pytest harness).
2. Define CI steps for skill signing and vulnerability scanning (Sigstore? Cosign?).
3. Assess telemetry sinks (OpenTelemetry collector vs. bespoke logging) compatible with FastRender trace IDs.
4. Prototype openclaw status MCP server contract and resilience tests (retry/backoff, mutual TLS).

## Tracking
- Update this log whenever new tooling decisions or research findings emerge.
- Cross-link new documents (plans, tasks, runbooks) referencing Constitution principles to maintain traceability.

## Tool Usage Log
- 2026-02-06 12:00 UTC – Ran `get_changed_files` to confirm working tree edits before summarizing speckit.plan deliverables.
- 2026-02-06 12:00 UTC – Triggered `log_passage_time_trigger` per governance workflow to capture planning context prior to responding.
- 2026-02-06 12:05 UTC – Updated `.github/copilot-instructions.md` via `apply_patch` to codify speckit rule invocation and Tenx MCP logging requirements.
- 2026-02-06 12:07 UTC – Edited `.github/copilot-instructions.md` to mandate use of git MCP tooling for repository interactions.
