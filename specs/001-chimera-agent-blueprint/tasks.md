# Tasks: Chimera Autonomous Influencer Network

**Input**: Design documents from `/specs/001-chimera-agent-blueprint/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: This implementation uses Test-Driven Development (TDD) with contract tests and integration tests as specified in plan.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md, the project follows this structure:
- **Source**: `src/chimera/` (planner, worker, judge, skills, shared, cli)
- **Tests**: `tests/` (unit, integration, contract)
- **Configs**: `configs/`
- **Scripts**: `scripts/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the Chimera autonomous agent system

- [ ] T001 Create project directory structure per plan.md: src/chimera/{planner,worker,judge,skills/openclaw,shared/{contracts,telemetry},cli}
- [ ] T002 Initialize Python 3.11 project with pyproject.toml and configure uv/poetry dependencies (CrewAI, LangGraph, FastAPI, SQLAlchemy, Redis-py, Weaviate, Coinbase AgentKit, MCP Python SDK, Pydantic, pytest)
- [ ] T003 [P] Create docker-compose.yml for infrastructure services (PostgreSQL 16 + pgvector, Redis, Weaviate, LocalStack)
- [ ] T004 [P] Configure ruff linting and pyright type checking in pyproject.toml
- [ ] T005 [P] Setup GitHub Actions CI/CD workflow in .github/workflows/chimera-ci.yml
- [ ] T006 [P] Create .env.example with MCP endpoints, Coinbase keys, OpenClaw TLS configuration
- [ ] T007 [P] Setup Makefile with infra-up, infra-down, test, lint targets
- [ ] T008 Create test directory structure: tests/{unit/{planner,worker,judge},integration/{swarm,openclaw},contract/mcp_servers}

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Storage Infrastructure

- [ ] T009 Create Alembic migration framework in src/chimera/shared/migrations/
- [ ] T010 Create initial migration for agents table with base schema (agent_id, persona_slug, status_snapshot, created_at, updated_at)
- [ ] T011 [P] Add migration for TrendSignal table (signal_id, agent_id, resource_uri, trace_id, relevance_score, campaign_hint, payload, ingested_at)
- [ ] T012 [P] Add migration for AgentTask extended schema (task_id, agent_id, confidence_window, persona_lock, budget_cap_usd, hitl_ticket_id, openclaw_request_id, state, state_version, result_artifact)
- [ ] T013 [P] Add migration for OpenClawStatusLog table (status_id, agent_id, payload, presence_state, ack_trace_id, wallet_band, signature, state_version, broadcast_at, ack_latency_ms)
- [ ] T014 [P] Add migration for WalletLedger table (ledger_id, agent_id, intent_source, amount_usd, risk_score, cfo_decision, created_at)
- [ ] T015 [P] Add migration for HITLQueueItem table (ticket_id, task_id, confidence_score, sensitive_topics, reasoning_trace, artifact_ref, assigned_to, sla_expires_at, created_at)
- [ ] T016 Run Alembic migrations and verify all tables with pgvector extension in local PostgreSQL

### Shared Domain Models

- [ ] T017 [P] Create base Pydantic models in src/chimera/shared/contracts/base.py (TraceContext, StateVersion, BudgetCap)
- [ ] T018 [P] Create TrendSignal domain model in src/chimera/shared/contracts/trend_signal.py
- [ ] T019 [P] Create AgentTask domain model in src/chimera/shared/contracts/agent_task.py (with state transitions)
- [ ] T020 [P] Create OpenClawStatus domain model in src/chimera/shared/contracts/openclaw_status.py (matching contracts/openclaw-status.json)
- [ ] T021 [P] Create WalletIntent domain model in src/chimera/shared/contracts/wallet.py
- [ ] T022 [P] Create HITLTicket domain model in src/chimera/shared/contracts/hitl.py

### Telemetry & Observability

- [ ] T023 [P] Implement trace ID propagation utilities in src/chimera/shared/telemetry/tracing.py
- [ ] T024 [P] Create structured logging configuration in src/chimera/shared/telemetry/logging.py
- [ ] T025 [P] Setup metrics collection framework in src/chimera/shared/telemetry/metrics.py (Prometheus-compatible)

### Redis Queue Infrastructure

- [ ] T026 Create Redis connection manager in src/chimera/shared/redis_client.py
- [ ] T027 [P] Implement task queue abstraction in src/chimera/shared/queues/task_queue.py
- [ ] T028 [P] Implement HITL queue abstraction in src/chimera/shared/queues/hitl_queue.py
- [ ] T029 [P] Implement spend counter with budget decorators in src/chimera/shared/redis_spend.py

### Database Repository Layer

- [ ] T030 [P] Create SQLAlchemy session factory in src/chimera/shared/db.py with OCC support
- [ ] T031 [P] Implement TrendSignal repository in src/chimera/shared/repositories/trend_signal_repo.py
- [ ] T032 [P] Implement AgentTask repository in src/chimera/shared/repositories/agent_task_repo.py (with state_version validation)
- [ ] T033 [P] Implement OpenClawStatusLog repository in src/chimera/shared/repositories/openclaw_status_repo.py
- [ ] T034 [P] Implement WalletLedger repository in src/chimera/shared/repositories/wallet_ledger_repo.py
- [ ] T035 [P] Implement HITLQueueItem repository in src/chimera/shared/repositories/hitl_repo.py

### Configuration & Environment

- [ ] T036 [P] Create configuration loader in src/chimera/shared/config.py (loads from YAML + env vars)
- [ ] T037 [P] Create planner config schema in configs/planner.yaml
- [ ] T038 [P] Create worker config schema in configs/worker.yaml
- [ ] T039 [P] Create judge config schema in configs/judge.yaml
- [ ] T040 [P] Create OpenClaw MCP server config schema in configs/openclaw.yaml

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Planner Detects Trends (Priority: P1) 🎯 MVP

**Goal**: Enable Planner agent to continuously ingest MCP resources, score relevance, and create DAG tasks for high-value trends (relevance ≥0.75) without human prompting

**Independent Test**: Feed synthetic MCP resource updates with varying relevance scores; verify only qualifying events (≥0.75) spawn tasks with trace IDs visible on the Operator dashboard

### Contract Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T041 [P] [US1] Create contract test for MCP resource polling endpoint in tests/contract/mcp_servers/test_resource_ingestion.py
- [ ] T042 [P] [US1] Create contract test for DAG task creation API in tests/contract/test_planner_task_creation.py

### Integration Tests for User Story 1

- [ ] T043 [P] [US1] Create integration test for end-to-end trend detection flow in tests/integration/swarm/test_trend_to_task.py (synthetic feed → task creation)
- [ ] T044 [P] [US1] Create integration test for OCC state_version validation during paused campaigns in tests/integration/swarm/test_campaign_pause.py

### Implementation for User Story 1

- [ ] T045 [P] [US1] Implement MCP resource client in src/chimera/planner/mcp_resource_client.py (polls MCP endpoints, handles rate limiting)
- [ ] T046 [P] [US1] Implement semantic relevance scorer using Gemini 3 Flash in src/chimera/planner/relevance_scorer.py
- [ ] T047 [US1] Create Planner service class in src/chimera/planner/planner_service.py (orchestrates polling → scoring → task creation)
- [ ] T048 [US1] Implement trend-to-task converter in src/chimera/planner/task_factory.py (generates DAG tasks with trace IDs, persona locks, budget caps)
- [ ] T049 [US1] Add OCC state_version validation in src/chimera/planner/campaign_state.py (checks campaign pause status)
- [ ] T050 [US1] Create Planner FastAPI app in src/chimera/planner/app.py with /health and /metrics endpoints
- [ ] T051 [US1] Implement governor limits for daily task caps in src/chimera/planner/governor.py (queues alerts when thresholds exceeded)
- [ ] T052 [US1] Add retry logic with exponential backoff for MCP feed failures in src/chimera/planner/retry_policy.py
- [ ] T053 [US1] Create telemetry logging for trend detection pipeline in src/chimera/planner/telemetry.py (logs trace_id, relevance_score, task_id)
- [ ] T054 [US1] Add Planner CLI commands in src/chimera/cli/planner_cli.py (replay-trends, check-governor, view-signals)

### Unit Tests for User Story 1

- [ ] T055 [P] [US1] Unit test for relevance scorer in tests/unit/planner/test_relevance_scorer.py
- [ ] T056 [P] [US1] Unit test for task factory in tests/unit/planner/test_task_factory.py
- [ ] T057 [P] [US1] Unit test for governor limits in tests/unit/planner/test_governor.py
- [ ] T058 [P] [US1] Unit test for OCC validation in tests/unit/planner/test_campaign_state.py

**Checkpoint**: At this point, Planner can autonomously detect trends and create tasks. Verify with `scripts/seed_trends.py --scenario fashion_drop`

---

## Phase 4: User Story 2 - Worker Generates Multi-Modal Artifacts (Priority: P1) 🎯 MVP

**Goal**: Enable Worker agents to execute DAG tasks, generate text/image/video content matching persona constraints with character lock IDs, and prepare artifacts for Judge review

**Independent Test**: Provide a DAG with a `generate_content` node, mock MCP tool calls, assert outputs include persona locks, cost telemetry, and attachments for Judge validation

### Contract Tests for User Story 2

- [ ] T059 [P] [US2] Create contract test for MCP content generation tools (text, image, video) in tests/contract/mcp_servers/test_content_generation.py
- [ ] T060 [P] [US2] Create contract test for Worker artifact submission API in tests/contract/test_worker_artifact_submission.py

### Integration Tests for User Story 2

- [ ] T061 [P] [US2] Create integration test for multi-modal content generation pipeline in tests/integration/swarm/test_worker_content_generation.py
- [ ] T062 [P] [US2] Create integration test for budget telemetry tracking in tests/integration/swarm/test_worker_budget_tracking.py

### Implementation for User Story 2

- [ ] T063 [P] [US2] Implement MCP content tool client in src/chimera/worker/mcp_content_client.py (calls text, image, video generation with character_reference_id)
- [ ] T064 [P] [US2] Create Worker task executor in src/chimera/worker/task_executor.py (consumes Redis task queue, executes DAG nodes)
- [ ] T065 [US2] Implement persona constraint validator in src/chimera/worker/persona_validator.py (checks content adherence to SOUL.md directives)
- [ ] T066 [US2] Create cost telemetry collector in src/chimera/worker/cost_tracker.py (tracks MCP tool usage, API costs per task)
- [ ] T067 [US2] Implement artifact builder in src/chimera/worker/artifact_builder.py (packages text/image/video with metadata, locks, trace IDs)
- [ ] T068 [US2] Create Worker FastAPI app in src/chimera/worker/app.py with /health, /metrics, /task-status endpoints
- [ ] T069 [US2] Add Worker pool manager in src/chimera/worker/pool_manager.py (scales workers based on queue depth)
- [ ] T070 [US2] Implement result submission to Judge queue in src/chimera/worker/result_submitter.py
- [ ] T071 [US2] Add error handling for MCP tool failures in src/chimera/worker/error_handler.py (retries, dead-letter queue)
- [ ] T072 [US2] Create Worker CLI commands in src/chimera/cli/worker_cli.py (start-pool, check-queue, retry-failed)

### Unit Tests for User Story 2

- [ ] T073 [P] [US2] Unit test for persona validator in tests/unit/worker/test_persona_validator.py
- [ ] T074 [P] [US2] Unit test for cost tracker in tests/unit/worker/test_cost_tracker.py
- [ ] T075 [P] [US2] Unit test for artifact builder in tests/unit/worker/test_artifact_builder.py
- [ ] T076 [P] [US2] Unit test for error handler in tests/unit/worker/test_error_handler.py

**Checkpoint**: Workers can generate multi-modal content with persona locks. Verify artifacts stored with `SELECT * FROM agent_tasks WHERE state = 'JUDGE_REVIEW';`

---

## Phase 5: User Story 3 - HITL Safety & Governance (Priority: P1) 🎯 MVP

**Goal**: Enable Judge agents to evaluate Worker artifacts using confidence thresholds (≥0.90 auto-approve, 0.70-0.90 HITL, <0.70 reject), route to HITL queue when needed, and enforce sensitive topic overrides

**Independent Test**: Submit artifacts with varying confidence scores and sensitive topics; verify routing decisions match thresholds, HITL queue populated correctly, and reasoning traces available

**Note**: This story was re-prioritized to P1 as it's critical for MVP safety and governance (originally US3 in spec.md, combined HITL aspects)

### Contract Tests for User Story 3

- [ ] T077 [P] [US3] Create contract test for Judge confidence evaluation API in tests/contract/test_judge_evaluation.py
- [ ] T078 [P] [US3] Create contract test for HITL queue API in tests/contract/test_hitl_queue_api.py

### Integration Tests for User Story 3

- [ ] T079 [P] [US3] Create integration test for Judge auto-approval flow in tests/integration/swarm/test_judge_auto_approve.py
- [ ] T080 [P] [US3] Create integration test for HITL routing and SLA tracking in tests/integration/swarm/test_judge_hitl_routing.py
- [ ] T081 [P] [US3] Create integration test for sensitive topic override in tests/integration/swarm/test_judge_sensitive_topics.py

### Implementation for User Story 3

- [ ] T082 [P] [US3] Implement confidence scorer in src/chimera/judge/confidence_scorer.py (evaluates artifact quality, persona adherence)
- [ ] T083 [P] [US3] Create sensitive topic detector in src/chimera/judge/sensitive_detector.py (scans for configured sensitive keywords/topics)
- [ ] T084 [US3] Implement Judge decision engine in src/chimera/judge/decision_engine.py (applies thresholds, routes to auto/HITL/reject)
- [ ] T085 [US3] Create reasoning trace generator in src/chimera/judge/reasoning_trace.py (logs decision rationale, confidence breakdown)
- [ ] T086 [US3] Implement HITL queue manager in src/chimera/judge/hitl_manager.py (creates tickets, tracks SLA, escalates when >50 pending)
- [ ] T087 [US3] Create Judge FastAPI app in src/chimera/judge/app.py with /health, /metrics, /hitl/queue endpoints
- [ ] T088 [US3] Implement CFO Judge for budget validation in src/chimera/judge/cfo_judge.py (validates spend limits, risk scores)
- [ ] T089 [US3] Add auto-publish trigger for approved artifacts in src/chimera/judge/publish_trigger.py (queues MCP action tool calls)
- [ ] T090 [US3] Create HITL API endpoints in src/chimera/judge/hitl_api.py (GET /hitl/queue, POST /hitl/approve, POST /hitl/reject)
- [ ] T091 [US3] Add Judge CLI commands in src/chimera/cli/judge_cli.py (view-queue, approve-ticket, reject-ticket, check-sla)

### Unit Tests for User Story 3

- [ ] T092 [P] [US3] Unit test for confidence scorer in tests/unit/judge/test_confidence_scorer.py
- [ ] T093 [P] [US3] Unit test for sensitive detector in tests/unit/judge/test_sensitive_detector.py
- [ ] T094 [P] [US3] Unit test for decision engine in tests/unit/judge/test_decision_engine.py
- [ ] T095 [P] [US3] Unit test for HITL manager in tests/unit/judge/test_hitl_manager.py
- [ ] T096 [P] [US3] Unit test for CFO Judge in tests/unit/judge/test_cfo_judge.py

**Checkpoint**: Complete P1 MVP - Planner detects trends → Workers generate content → Judge evaluates with HITL safety. Test end-to-end with `pytest tests/integration/swarm -m replay`

---

## Phase 6: User Story 4 - OpenClaw Availability Broadcast (Priority: P2)

**Goal**: Enable Chimera agents to publish signed presence beacons (availability, campaign focus, wallet tier) to OpenClaw network and respond to collaboration intents through MCP

**Independent Test**: Simulate Planner telemetry changes, verify OpenClaw MCP server emits `status.publish_availability` payloads with valid signatures and receives acknowledgements

### Contract Tests for User Story 4

- [ ] T097 [P] [US4] Create contract test for OpenClaw status.publish_availability in tests/contract/mcp_servers/test_openclaw_publish.py (validate against contracts/openclaw-status.json)
- [ ] T098 [P] [US4] Create contract test for OpenClaw status.revoke in tests/contract/mcp_servers/test_openclaw_revoke.py
- [ ] T099 [P] [US4] Create contract test for OpenClaw status.fetch_neighbors in tests/contract/mcp_servers/test_openclaw_fetch.py

### Integration Tests for User Story 4

- [ ] T100 [P] [US4] Create integration test for availability broadcast pipeline in tests/integration/openclaw/test_status_broadcast.py
- [ ] T101 [P] [US4] Create integration test for collaboration intent handling in tests/integration/openclaw/test_collab_intent.py
- [ ] T102 [P] [US4] Create integration test for credential rotation after compromise in tests/integration/openclaw/test_credential_rotation.py

### Implementation for User Story 4

- [ ] T103 [P] [US4] Create OpenClaw MCP server scaffold in src/chimera/skills/openclaw/server.py (MCP protocol handler)
- [ ] T104 [P] [US4] Implement AgentKit wallet integration in src/chimera/skills/openclaw/wallet_client.py (signs payloads with CDP keys)
- [ ] T105 [US4] Implement status.publish_availability tool in src/chimera/skills/openclaw/tools/publish_availability.py
- [ ] T106 [US4] Implement status.revoke tool in src/chimera/skills/openclaw/tools/revoke_status.py
- [ ] T107 [US4] Implement status.fetch_neighbors tool in src/chimera/skills/openclaw/tools/fetch_neighbors.py
- [ ] T108 [US4] Create OpenClaw status payload builder in src/chimera/skills/openclaw/payload_builder.py (formats beacon per contract schema)
- [ ] T109 [US4] Implement signature validator in src/chimera/skills/openclaw/signature_validator.py (verifies incoming signatures)
- [ ] T110 [US4] Add acknowledgement tracking in src/chimera/skills/openclaw/ack_tracker.py (logs ack_latency_ms for SLO monitoring)
- [ ] T111 [US4] Create Planner integration hook in src/chimera/planner/openclaw_publisher.py (triggers broadcasts on state changes)
- [ ] T112 [US4] Implement collaboration intent validator in src/chimera/skills/openclaw/intent_validator.py (pre-checks budget, risk)
- [ ] T113 [US4] Add CFO Judge integration for OpenClaw intents in src/chimera/judge/openclaw_cfo.py (validates before Planner accepts)
- [ ] T114 [US4] Create OpenClaw MCP server CLI in src/chimera/cli/openclaw_cli.py (start-server, publish-status, verify-signature)

### Unit Tests for User Story 4

- [ ] T115 [P] [US4] Unit test for payload builder in tests/unit/skills/openclaw/test_payload_builder.py
- [ ] T116 [P] [US4] Unit test for signature validator in tests/unit/skills/openclaw/test_signature_validator.py
- [ ] T117 [P] [US4] Unit test for ack tracker in tests/unit/skills/openclaw/test_ack_tracker.py
- [ ] T118 [P] [US4] Unit test for intent validator in tests/unit/skills/openclaw/test_intent_validator.py

**Checkpoint**: Agents can broadcast presence to OpenClaw network. Verify with `scripts/publish_status.py --agent chimera-fae` and check `openclaw_status_log` table

---

## Phase 7: User Story 5 - Agentic Commerce Controls (Priority: P2)

**Goal**: Enable CFO Judge to validate all OpenClaw collaboration intents and wallet transfers using risk scoring, budget governors, and ledger persistence before Planner schedules work

**Independent Test**: Submit collaboration intents with varying risk scores and budget levels; verify CFO Judge approvals/rejections follow policy, ledger records persist, and alerts trigger for violations

### Contract Tests for User Story 5

- [ ] T119 [P] [US5] Create contract test for wallet transfer API in tests/contract/test_wallet_transfer.py
- [ ] T120 [P] [US5] Create contract test for budget governor API in tests/contract/test_budget_governor.py

### Integration Tests for User Story 5

- [ ] T121 [P] [US5] Create integration test for CFO approval flow in tests/integration/swarm/test_cfo_approval.py
- [ ] T122 [P] [US5] Create integration test for budget governor enforcement in tests/integration/swarm/test_budget_enforcement.py
- [ ] T123 [P] [US5] Create integration test for wallet ledger reconciliation in tests/integration/swarm/test_ledger_reconciliation.py

### Implementation for User Story 5

- [ ] T124 [P] [US5] Extend CFO Judge with risk scoring engine in src/chimera/judge/cfo_risk_scorer.py (evaluates intent_source, amount, agent reputation)
- [ ] T125 [US5] Implement budget governor with Redis counters in src/chimera/judge/budget_governor.py (tracks daily/hourly spend, enforces $50 default cap)
- [ ] T126 [US5] Create wallet ledger writer in src/chimera/judge/ledger_writer.py (persists all approved/rejected transactions)
- [ ] T127 [US5] Add CFO decision API endpoints in src/chimera/judge/cfo_api.py (GET /cfo/decisions, POST /cfo/validate-intent)
- [ ] T128 [US5] Implement Operator alert system in src/chimera/judge/operator_alerts.py (triggers when risk_score >0.7 or budget exceeded)
- [ ] T129 [US5] Create blockchain ledger sync in src/chimera/skills/openclaw/ledger_sync.py (reconciles PostgreSQL with AgentKit wallet)
- [ ] T130 [US5] Add spend counter decorators in src/chimera/shared/decorators/spend_tracker.py (wraps functions to auto-track costs)
- [ ] T131 [US5] Create CFO CLI commands in src/chimera/cli/cfo_cli.py (view-ledger, check-budget, reconcile-wallet, force-approve)

### Unit Tests for User Story 5

- [ ] T132 [P] [US5] Unit test for CFO risk scorer in tests/unit/judge/test_cfo_risk_scorer.py
- [ ] T133 [P] [US5] Unit test for budget governor in tests/unit/judge/test_budget_governor.py
- [ ] T134 [P] [US5] Unit test for ledger writer in tests/unit/judge/test_ledger_writer.py
- [ ] T135 [P] [US5] Unit test for spend counter decorator in tests/unit/shared/test_spend_tracker.py

**Checkpoint**: Agentic commerce fully protected with CFO Judge validation. Test with collaboration intents exceeding budget limits

---

## Phase 8: User Story 6 - Engagement Loop Automation (Priority: P2)

**Goal**: Enable Workers to monitor post-publication engagement metrics (likes, comments, shares) and trigger follow-up content tasks based on configurable thresholds without human intervention

**Independent Test**: Publish content, simulate engagement events via MCP, verify Workers autonomously create follow-up tasks when thresholds met (e.g., >1000 likes → create thread continuation)

### Contract Tests for User Story 6

- [ ] T136 [P] [US6] Create contract test for MCP engagement monitoring tools in tests/contract/mcp_servers/test_engagement_monitor.py
- [ ] T137 [P] [US6] Create contract test for follow-up task creation API in tests/contract/test_followup_tasks.py

### Integration Tests for User Story 6

- [ ] T138 [P] [US6] Create integration test for engagement-triggered content in tests/integration/swarm/test_engagement_loop.py
- [ ] T139 [P] [US6] Create integration test for engagement threshold configuration in tests/integration/swarm/test_engagement_thresholds.py

### Implementation for User Story 6

- [ ] T140 [P] [US6] Create engagement metrics collector in src/chimera/worker/engagement_collector.py (polls MCP for likes, comments, shares)
- [ ] T141 [P] [US6] Implement threshold evaluator in src/chimera/worker/threshold_evaluator.py (checks if metrics exceed configured limits)
- [ ] T142 [US6] Create follow-up task generator in src/chimera/worker/followup_generator.py (spawns continuation, reply, or amplification tasks)
- [ ] T143 [US6] Add engagement monitoring loop in src/chimera/worker/engagement_monitor.py (background poller for published content)
- [ ] T144 [US6] Implement engagement telemetry in src/chimera/worker/engagement_telemetry.py (logs metric trends, alerts on viral content)
- [ ] T145 [US6] Create engagement configuration schema in configs/engagement_thresholds.yaml
- [ ] T146 [US6] Add engagement CLI commands in src/chimera/cli/engagement_cli.py (view-metrics, configure-thresholds, test-trigger)

### Unit Tests for User Story 6

- [ ] T147 [P] [US6] Unit test for threshold evaluator in tests/unit/worker/test_threshold_evaluator.py
- [ ] T148 [P] [US6] Unit test for follow-up generator in tests/unit/worker/test_followup_generator.py
- [ ] T149 [P] [US6] Unit test for engagement telemetry in tests/unit/worker/test_engagement_telemetry.py

**Checkpoint**: Engagement loops running autonomously. Simulate viral content and verify follow-up tasks created

---

## Phase 9: User Story 7 - Developer Extensibility (Priority: P3)

**Goal**: Provide SDK and plugin system for developers to add custom MCP tools, trend scorers, and content generators without modifying core Chimera code

**Independent Test**: Create sample plugin that adds a new trend source, register it via config, verify Planner ingests and processes the custom source

### Contract Tests for User Story 7

- [ ] T150 [P] [US7] Create contract test for plugin registration API in tests/contract/test_plugin_registration.py
- [ ] T151 [P] [US7] Create contract test for plugin lifecycle hooks in tests/contract/test_plugin_lifecycle.py

### Integration Tests for User Story 7

- [ ] T152 [P] [US7] Create integration test for custom trend scorer plugin in tests/integration/plugins/test_custom_scorer.py
- [ ] T153 [P] [US7] Create integration test for custom content generator plugin in tests/integration/plugins/test_custom_generator.py

### Implementation for User Story 7

- [ ] T154 [P] [US7] Create plugin interface definitions in src/chimera/shared/plugins/interfaces.py (TrendScorerPlugin, ContentGeneratorPlugin, MCPToolPlugin)
- [ ] T155 [P] [US7] Implement plugin registry in src/chimera/shared/plugins/registry.py (discovers and loads plugins from configured paths)
- [ ] T156 [US7] Create plugin loader with lifecycle hooks in src/chimera/shared/plugins/loader.py (init, start, stop, health checks)
- [ ] T157 [US7] Add plugin configuration schema in src/chimera/shared/plugins/config_schema.py
- [ ] T158 [US7] Integrate plugin system into Planner in src/chimera/planner/plugin_integration.py (allows custom trend scorers)
- [ ] T159 [US7] Integrate plugin system into Worker in src/chimera/worker/plugin_integration.py (allows custom content generators)
- [ ] T160 [US7] Create example plugins in examples/plugins/{custom_scorer,custom_generator,custom_mcp_tool}/
- [ ] T161 [US7] Add plugin CLI commands in src/chimera/cli/plugin_cli.py (list-plugins, install-plugin, enable-plugin, disable-plugin)
- [ ] T162 [US7] Create plugin developer documentation in docs/developer-guide/plugins.md

### Unit Tests for User Story 7

- [ ] T163 [P] [US7] Unit test for plugin registry in tests/unit/shared/test_plugin_registry.py
- [ ] T164 [P] [US7] Unit test for plugin loader in tests/unit/shared/test_plugin_loader.py
- [ ] T165 [P] [US7] Unit test for example plugins in tests/unit/plugins/test_example_plugins.py

**Checkpoint**: Plugin system fully functional. Test by installing example plugins and verifying they execute correctly

---

## Phase 10: User Story 8 - Persona Evolution Feedback (Priority: P3)

**Goal**: Enable system to track artifact performance metrics (engagement, conversions) and suggest SOUL.md persona adjustments based on what content resonates most with audiences

**Independent Test**: Publish diverse content with different persona tones, collect engagement metrics, verify system generates persona evolution suggestions with supporting data

### Contract Tests for User Story 8

- [ ] T166 [P] [US8] Create contract test for persona analytics API in tests/contract/test_persona_analytics.py
- [ ] T167 [P] [US8] Create contract test for persona suggestion API in tests/contract/test_persona_suggestions.py

### Integration Tests for User Story 8

- [ ] T168 [P] [US8] Create integration test for persona performance tracking in tests/integration/swarm/test_persona_tracking.py
- [ ] T169 [P] [US8] Create integration test for persona evolution suggestions in tests/integration/swarm/test_persona_evolution.py

### Implementation for User Story 8

- [ ] T170 [P] [US8] Create artifact performance tracker in src/chimera/judge/performance_tracker.py (links artifacts to engagement metrics)
- [ ] T171 [P] [US8] Implement persona analytics engine in src/chimera/judge/persona_analytics.py (analyzes which persona traits correlate with high engagement)
- [ ] T172 [US8] Create persona evolution suggester in src/chimera/judge/evolution_suggester.py (generates SOUL.md change recommendations)
- [ ] T173 [US8] Add Weaviate semantic memory integration in src/chimera/shared/weaviate_client.py (stores artifact embeddings for similarity analysis)
- [ ] T174 [US8] Implement persona A/B testing framework in src/chimera/worker/persona_ab_test.py (tests persona variations)
- [ ] T175 [US8] Create persona analytics API endpoints in src/chimera/judge/persona_api.py (GET /persona/analytics, GET /persona/suggestions)
- [ ] T176 [US8] Add persona evolution UI dashboard data endpoints in src/chimera/judge/dashboard_data.py
- [ ] T177 [US8] Create persona CLI commands in src/chimera/cli/persona_cli.py (view-analytics, suggest-evolution, apply-suggestion)

### Unit Tests for User Story 8

- [ ] T178 [P] [US8] Unit test for performance tracker in tests/unit/judge/test_performance_tracker.py
- [ ] T179 [P] [US8] Unit test for persona analytics in tests/unit/judge/test_persona_analytics.py
- [ ] T180 [P] [US8] Unit test for evolution suggester in tests/unit/judge/test_evolution_suggester.py
- [ ] T181 [P] [US8] Unit test for persona A/B testing in tests/unit/worker/test_persona_ab_test.py

**Checkpoint**: Persona evolution system active. Review suggestions after sufficient engagement data collected

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, documentation, and production readiness

### Documentation

- [ ] T182 [P] Create comprehensive README.md for project with architecture overview
- [ ] T183 [P] Document API endpoints in docs/api-reference.md (OpenAPI/Swagger specs)
- [ ] T184 [P] Create operator guide in docs/operator-guide.md (deployment, monitoring, troubleshooting)
- [ ] T185 [P] Document MCP server integration patterns in docs/mcp-integration.md
- [ ] T186 [P] Create security and compliance guide in docs/security.md (key management, audit logs)

### Production Readiness

- [ ] T187 [P] Add health check endpoints to all services (Planner, Worker, Judge, OpenClaw MCP)
- [ ] T188 [P] Implement graceful shutdown handlers in all services
- [ ] T189 [P] Add Prometheus metrics exporters to all services
- [ ] T190 [P] Create Grafana dashboards for operational metrics in monitoring/grafana/dashboards/
- [ ] T191 Create Kubernetes deployment manifests in k8s/ (deployments, services, configmaps, secrets)
- [ ] T192 [P] Add horizontal pod autoscaling configuration based on queue depth metrics
- [ ] T193 [P] Setup log aggregation with structured JSON logging
- [ ] T194 [P] Implement distributed tracing with OpenTelemetry integration

### Performance & Optimization

- [ ] T195 [P] Add database connection pooling optimization
- [ ] T196 [P] Implement Redis caching for frequently accessed data (agent status, campaign configs)
- [ ] T197 [P] Add batch processing for OpenClaw status broadcasts (reduce network overhead)
- [ ] T198 [P] Optimize Weaviate queries for semantic search performance
- [ ] T199 Performance testing and benchmark suite in tests/performance/

### Security & Compliance

- [ ] T200 [P] Implement secret rotation mechanism for MCP credentials
- [ ] T201 [P] Add audit logging for all CFO Judge decisions
- [ ] T202 [P] Implement rate limiting on public-facing APIs
- [ ] T203 [P] Add input validation and sanitization across all endpoints
- [ ] T204 Setup dependency vulnerability scanning in CI/CD

### Testing & Quality

- [ ] T205 [P] Increase unit test coverage to >80% across all modules
- [ ] T206 Create end-to-end smoke tests for production deployments in tests/e2e/
- [ ] T207 [P] Add mutation testing to verify test quality
- [ ] T208 Create data migration testing framework in tests/migrations/
- [ ] T209 Setup contract regression testing for MCP servers

### Operational Scripts

- [ ] T210 [P] Create backup and restore scripts in scripts/backup_restore.py
- [ ] T211 [P] Create database migration rollback utility in scripts/rollback_migration.py
- [ ] T212 [P] Create operational dashboard seed data script in scripts/seed_dashboard_data.py
- [ ] T213 [P] Create synthetic test data generator in scripts/generate_test_data.py
- [ ] T214 Create disaster recovery runbook in docs/runbooks/disaster-recovery.md

### Quickstart Validation

- [ ] T215 Run complete quickstart.md validation (setup → services → tests → operational workflow)
- [ ] T216 Verify all quickstart troubleshooting scenarios work correctly
- [ ] T217 Update quickstart.md with any discovered gaps or corrections

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP critical path starts here
- **User Story 2 (Phase 4)**: Depends on Foundational + US1 (needs tasks from Planner)
- **User Story 3 (Phase 5)**: Depends on Foundational + US2 (needs artifacts from Workers) - MVP critical path
- **User Story 4 (Phase 6)**: Depends on Foundational + US1 (needs Planner state changes) - Post-MVP
- **User Story 5 (Phase 7)**: Depends on Foundational + US4 (needs OpenClaw integration) - Post-MVP
- **User Story 6 (Phase 8)**: Depends on Foundational + US2 (needs published content) - Post-MVP
- **User Story 7 (Phase 9)**: Depends on Foundational only (independent extensibility) - Post-MVP
- **User Story 8 (Phase 10)**: Depends on Foundational + US2 + US6 (needs engagement data) - Post-MVP
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

**MVP Critical Path (P1):**
- US1 (Planner Detects Trends) → US2 (Worker Generates Content) → US3 (HITL Safety & Governance)
- These three stories MUST be completed in sequence for a functional MVP
- MVP Success Criteria: Autonomous trend detection → multi-modal content generation → safety governance

**Post-MVP (P2):**
- US4 (OpenClaw Availability) - Can start after US1 (independent of content generation)
- US5 (Agentic Commerce) - Requires US4 (OpenClaw integration)
- US6 (Engagement Loop) - Requires US2 (published content to monitor)

**Future Enhancements (P3):**
- US7 (Developer Extensibility) - Independent, can start after Foundational
- US8 (Persona Evolution) - Requires US2 + US6 (needs engagement data)

### Within Each User Story

1. Contract tests FIRST (write and verify they FAIL)
2. Integration tests (write and verify they FAIL)
3. Core implementation (make tests PASS)
4. Unit tests (additional coverage)
5. Story validation checkpoint

### Parallel Opportunities

**Within Phases:**
- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- All contract tests within a user story marked [P] can run in parallel
- All integration tests within a user story marked [P] can run in parallel
- All unit tests within a user story marked [P] can run in parallel

**Across Phases (with sufficient team capacity):**
- After Foundational completes:
  - US1 must complete first (critical path)
  - US2 starts after US1
  - US3 starts after US2
- After MVP (US1-US3) completes:
  - US4, US6, US7 can run in parallel (independent workstreams)
  - US5 waits for US4
  - US8 waits for US6

---

## Parallel Example: User Story 1 (Planner Detects Trends)

```bash
# Phase: Contract Tests (can all run simultaneously)
Team Member A: T041 - Contract test for MCP resource polling
Team Member B: T042 - Contract test for DAG task creation

# Phase: Integration Tests (can all run simultaneously)
Team Member A: T043 - Integration test for trend detection flow
Team Member B: T044 - Integration test for OCC validation

# Phase: Core Implementation (some parallelism)
Team Member A: T045 - MCP resource client
Team Member B: T046 - Semantic relevance scorer
# Then both complete before:
Team Members A+B: T047 - Planner service (integrates both)

# Phase: Supporting Implementation (parallel)
Team Member A: T048 - Task factory
Team Member B: T049 - OCC validation
Team Member C: T050 - FastAPI app
Team Member D: T051 - Governor limits

# Phase: Unit Tests (all parallel)
Team Member A: T055 - Test relevance scorer
Team Member B: T056 - Test task factory
Team Member C: T057 - Test governor
Team Member D: T058 - Test OCC validation
```

---

## Implementation Strategy

### MVP First (US1 → US2 → US3 Only)

**Goal**: Deliver autonomous trend-aware content generation with HITL safety in ~4-6 weeks

1. **Week 1**: Complete Phase 1 (Setup) + Phase 2 (Foundational)
   - Validate: Infrastructure running, migrations applied, shared libraries functional
2. **Week 2-3**: Complete Phase 3 (US1 - Planner Detects Trends)
   - Validate: Planner autonomously creates tasks from MCP resources
   - Test: `scripts/seed_trends.py --scenario fashion_drop`
3. **Week 3-4**: Complete Phase 4 (US2 - Worker Generates Content)
   - Validate: Workers produce multi-modal artifacts with persona locks
   - Test: Check `agent_tasks` table for completed artifacts
4. **Week 4-5**: Complete Phase 5 (US3 - HITL Safety & Governance)
   - Validate: Judge routes artifacts correctly, HITL queue functional
   - Test: End-to-end replay with `pytest tests/integration/swarm -m replay`
5. **Week 5-6**: Phase 11 (Critical Polish Only)
   - Focus: Production deployment, monitoring, documentation
   - Validate: `make quickstart` works end-to-end

**MVP Demo**: Show autonomous agent detecting fashion trend → generating Instagram post → Judge HITL approval → published

### Incremental Delivery (Post-MVP)

**Phase 6-7**: OpenClaw Network Integration (US4 + US5)
- Deliver: External agent coordination and commerce safeguards
- Timeline: +2-3 weeks
- Demo: Chimera agent broadcasting availability, responding to collaboration intents

**Phase 8**: Engagement Loop Automation (US6)
- Deliver: Self-sustaining content amplification
- Timeline: +1-2 weeks
- Demo: Viral content triggering follow-up posts automatically

**Phase 9-10**: Developer Experience (US7 + US8)
- Deliver: Plugin system and persona evolution
- Timeline: +2-3 weeks
- Demo: Custom plugin adds new trend source, persona evolves based on engagement

### Parallel Team Strategy (if 4-5 developers available)

**Phase 1-2 (Week 1)**: Entire team collaborates on Setup + Foundational
- Ensures everyone understands architecture
- Pair programming on complex pieces (OCC, migrations)

**Phase 3-5 (Week 2-5)**: Team splits by service
- Developer A: Planner (US1)
- Developer B: Worker (US2)
- Developer C: Judge (US3)
- Developer D: Testing + Integration (supports all)
- Meet daily for integration points

**Phase 6-10 (Week 6+)**: Team splits by user story
- Developer A+B: OpenClaw integration (US4 + US5)
- Developer C: Engagement loops (US6)
- Developer D: Extensibility (US7 + US8)

**Phase 11 (Final Week)**: Entire team on production readiness
- Everyone contributes to docs, polish, deployment

---

## Success Metrics

### MVP Success Criteria (Must achieve for US1-US3)

- **SC-001**: Planner converts ≥95% of high-relevance signals (≥0.75) into DAG tasks within 5 seconds
- **SC-002**: Worker + Judge pipeline produces multi-modal artifacts with <10 seconds median latency (excluding HITL)
- **SC-003**: HITL reviewers resolve queued artifacts within 2 hours; queue depth alerts trigger at 50 pending items
- **SC-004**: Confidence routing: ≥90% artifacts routed correctly (auto/HITL/reject) based on thresholds
- **SC-005**: Zero OCC state version conflicts in test scenarios

### Post-MVP Success Criteria (US4-US8)

- **SC-006**: OpenClaw availability beacons acknowledge within 1 minute with zero unsigned payloads
- **SC-007**: Budget governor violations detected within 60 seconds and logged with actionable reason codes
- **SC-008**: CFO Judge risk scoring rejects ≥90% of high-risk intents (risk_score >0.7)
- **SC-009**: Engagement loops trigger follow-up tasks within 2 minutes of threshold breach
- **SC-010**: Plugin system supports loading custom trend scorers with <5% performance overhead

### Operational Metrics (Phase 11)

- **OM-001**: All services maintain >99.5% uptime in staging environment
- **OM-002**: Test coverage >80% across unit/integration/contract tests
- **OM-003**: End-to-end swarm replay tests complete in <2 minutes
- **OM-004**: Quickstart validation passes on fresh environment in <15 minutes
- **OM-005**: CI/CD pipeline (lint, test, security scan) completes in <10 minutes

---

## Notes

- **[P] Marker**: Task can run in parallel with other [P] tasks in the same phase (different files, no dependencies)
- **[Story] Label**: Maps task to specific user story for traceability and independent implementation
- **Test-First Approach**: Contract and integration tests written BEFORE implementation (TDD)
- **OCC Critical**: All state writes must validate `state_version` to prevent race conditions
- **Checkpoint Validation**: Stop at each user story checkpoint to validate independently before proceeding
- **MVP Focus**: Prioritize US1 → US2 → US3 for fastest time-to-value
- **Constitution Compliance**: All tasks align with MCP-Strict Interfaces, FastRender discipline, HITL governance
- **Commit Strategy**: Commit after each task or logical group; use feature branches per user story
- **Integration Points**: Pay special attention to Planner→Worker and Worker→Judge interfaces (task payloads, artifact formats)
- **Security**: Never commit secrets; use .env files and secret management (LocalStack in dev, proper secret store in prod)

---

## Quickstart Validation

Before marking the implementation complete, validate the entire quickstart workflow:

1. Fresh environment setup: `make infra-up && uv sync && alembic upgrade head`
2. Service startup: Planner, Worker, Judge, OpenClaw MCP server
3. Synthetic trend injection: `scripts/seed_trends.py --scenario fashion_drop`
4. Verify task creation in database
5. Verify artifact generation
6. Verify Judge routing and HITL queue
7. Run full test suite: `pytest tests/`
8. Check metrics dashboards (Grafana)
9. Validate troubleshooting scenarios from quickstart.md

**Expected Result**: Complete autonomous workflow from trend detection → content generation → safety review → publish decision

---

**Total Tasks**: 217
**MVP Tasks (US1-US3)**: T001-T096 (96 tasks)
**Post-MVP Tasks (US4-US8)**: T097-T181 (85 tasks)
**Polish Tasks**: T182-T217 (36 tasks)

**Estimated MVP Timeline**: 4-6 weeks (1 developer) or 2-3 weeks (4 developers in parallel)
**Estimated Full Implementation**: 10-14 weeks total
