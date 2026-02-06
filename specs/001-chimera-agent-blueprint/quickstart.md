# Quickstart – Chimera Autonomous Trend Analysis Agent

## Prerequisites
- Python 3.11 with uv/poetry or pipx.
- Docker + docker-compose (for Postgres, Redis, Weaviate local stacks).
- Access to MCP-compatible APIs (news feeds, social streams) and Coinbase AgentKit keys (set `CDP_API_KEY_NAME`, `CDP_API_KEY_PRIVATE_KEY`).
- OpenClaw sandbox credentials + certs for mutual TLS.

## Environment Setup
1. `make infra-up` → spins Postgres (w/ pgvector), Redis, Weaviate, LocalStack for secrets.
2. `uv sync` (or `poetry install`) → installs planner/worker/judge packages plus MCP SDKs.
3. Copy `.env.example` to `.env`, fill MCP server endpoints, Coinbase keys, OpenClaw TLS paths.
4. Run migrations: `alembic upgrade head` (adds TrendSignal, OpenClawStatusLog, ledger fields).

## Running Services
1. Start Planner service: `uv run python -m chimera.planner.app --config configs/planner.yaml`
2. Start Worker pool: `uv run python -m chimera.worker.app --config configs/worker.yaml`
3. Start Judge service: `uv run python -m chimera.judge.app --config configs/judge.yaml`
4. Launch `mcp-server-openclaw`: `uv run python -m chimera.skills.openclaw.server --config configs/openclaw.yaml`
5. Optional: `npm run dev --workspace hitl-console` to open HITL reviewer UI.

## Testing
- Unit tests: `pytest tests/unit`
- Integration (swarm replay): `pytest tests/integration/swarm -m replay`
- Contract tests for MCP servers: `pytest tests/contract/mcp_servers -k openclaw` or `npx newman run contracts/openclaw-status.postman.json`
- Lint + type check: `ruff check` + `pyright`

## Operational Workflow
1. Seed synthetic trends: `uv run scripts/seed_trends.py --scenario fashion_drop`
2. Observe Planner creating DAG tasks (logs + `task_queue` depth metrics).
3. Worker executes multi-modal generation; verify artifacts stored in S3/local storage and `result_artifact` JSON saved.
4. Judge outputs HITL decisions accessible via `/api/hitl/queue` → use console for approvals.
5. Trigger OpenClaw status broadcast: `uv run scripts/publish_status.py --agent chimera-fae`
6. Review `openclaw_status_log` table and Grafana dashboards for ack latency + confidence windows.

## Troubleshooting
- Planner stuck? Check `trend_signal` table for `state_version` conflicts; run `scripts/replay_trends.py`.
- HITL queue spike? Use console to reassign tickets and ensure sensitive-topic filters not misconfigured.
- OpenClaw ACK delays? Inspect `logs/openclaw_server.log`, confirm TLS cert validity, and verify signatures with `scripts/verify_status.py`.
