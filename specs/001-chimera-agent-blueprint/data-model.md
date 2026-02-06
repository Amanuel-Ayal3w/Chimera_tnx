# Data Model – Chimera Autonomous Trend Analysis Agent

## Entities

### TrendSignal
- **Fields**: `signal_id` (UUID, PK), `agent_id` (UUID, FK agents), `resource_uri` (TEXT), `trace_id` (UUID), `relevance_score` (NUMERIC 0–1), `campaign_hint` (TEXT), `payload` (JSONB), `ingested_at` (TIMESTAMP).
- **Relationships**: One `TrendSignal` can spawn many `AgentTask` rows via `tasks.parent_task_id`.
- **Validation Rules**: `relevance_score >= 0.75` required before conversion to DAG task; `trace_id` unique per resource event.

### AgentTask (Extended)
- **Fields** (additions vs. global schema): `confidence_window` (NUMERIC), `persona_lock` (VARCHAR), `budget_cap_usd` (NUMERIC), `hitl_ticket_id` (UUID), `openclaw_request_id` (UUID nullable).
- **Relationships**: Tasks reference `agents`, may include `openclaw_status_log` link for provenance.
- **State Transitions**: `PENDING → EXECUTING → JUDGE_REVIEW → (PUBLISHED | HIT_QUEUE | FAILED)` with OCC validation per commit.

### OpenClawStatusLog
- **Fields**: `status_id` (UUID, PK), `agent_id`, `payload` (JSONB), `presence_state` (ENUM), `ack_trace_id` (VARCHAR), `wallet_band` (ENUM), `signature` (BYTEA), `state_version` (BIGINT), `broadcast_at` (TIMESTAMP), `ack_latency_ms` (INT).
- **Relationships**: `agent_id` FK, `ack_trace_id` ties back to OpenClaw response metadata.
- **Validation Rules**: Signatures required, `presence_state` limited to {ONLINE, IDLE, BUSY, OFFLINE, QUARANTINED}; `ack_latency_ms` must be populated for SLO tracking.

### WalletLedger (Feature-Specific Fields)
- **Fields**: inherit base ledger schema plus `intent_source` (ENUM: `planner`, `openclaw`, `manual`), `risk_score` (NUMERIC), `cfo_decision` (ENUM: `approved`, `rejected`).
- **Validation Rules**: `risk_score > 0.7` triggers automatic rejection and Operator alert.

### HITLQueueItem
- **Fields**: `ticket_id` (UUID, PK), `task_id`, `confidence_score`, `sensitive_topics` (TEXT[]), `reasoning_trace` (TEXT), `artifact_ref` (JSONB), `assigned_to` (UUID optional), `sla_expires_at` (TIMESTAMP).
- **Validation Rules**: SLA = created_at + 2h; auto- escalate when expired.

## Relationships Overview
- `agents` 1→N `TrendSignal`, `AgentTask`, `OpenClawStatusLog`, `WalletLedger`.
- `AgentTask` 1→N `HITLQueueItem` (when multiple iterations needed).
- `OpenClawStatusLog` 1→N `openclaw_collab_requests` (future extension for inbound intents).

## State/Workflow Notes
- TrendSignal ingestion populates `TrendSignal`, then Planner writes new `AgentTask` referencing it.
- Worker completions update `tasks.result_artifact` + create optional `HITLQueueItem` entry when confidence <0.90 or sensitive topics triggered.
- OpenClaw broadcasts append to `OpenClawStatusLog` and update `agents.status_snapshot` cache for quick reads.
