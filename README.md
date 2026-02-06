# Project Chimera – Autonomous Influencer Network

## Mission Snapshot
Project Chimera is an autonomous influencer fleet that blends FastRender-style Planner → Worker → Judge swarms with strict Model Context Protocol (MCP) contracts. Each agent plans, creates, validates, and publishes multi-modal content while respecting budget governors, HITL safety checks, and OpenClaw-style social interoperability.

## Architecture Highlights
- **Hierarchical Swarm**: Planner decomposes OKRs into DAG tasks, Workers execute MCP-backed skills in parallel, Judges enforce persona + compliance before HITL/publish ([specs/technical.md](specs/technical.md)).
- **Data Fabric**: PostgreSQL + pgvector anchor structured/video metadata, Redis handles coordination, Weaviate stores semantic memory, and AgentKit wallets enforce governor limits.
- **Governance**: Confidence buckets (≥0.90 auto, 0.70–0.90 HITL, <0.70 reject) plus CodeRabbit AI review and Dockerized CI keep every change spec-aligned.

## Repository Map
| Path | Purpose |
| --- | --- |
| [specs/_meta.md](specs/_meta.md) | Vision, constraints, and OpenClaw alignment. |
| [specs/functional.md](specs/functional.md) | User stories for agents, operators, and HITL reviewers. |
| [specs/technical.md](specs/technical.md) | API contracts, data schemas, Agent Communication Protocol. |
| [specs/openclaw_integration.md](specs/openclaw_integration.md) | Status/availability broadcast plan for the Agent Social Network. |
| [research/architecture_strategy.md](research/architecture_strategy.md) | FastRender + data/observability strategy. |
| [research/tooling_strategy.md](research/tooling_strategy.md) | MCP tooling decisions and activity log. |
| [skills/](skills/README.md) | Runtime skill packages with IO contracts (fetch trends, generate multimodal artifacts, validate content). |
| [tests/](tests) | Intentional failing contract suites defining the “empty slots.” |
| [scripts/spec_check.py](scripts/spec_check.py) | Ensures required specs, skills, and tests exist. |
| [Dockerfile](Dockerfile) & [Makefile](Makefile) | Reproducible env + standardized commands. |
| [.github/workflows/main.yml](.github/workflows/main.yml) | CI pipeline running spec-check + dockerized tests. |
| [.coderabbit.yaml](.coderabbit.yaml) | AI review policy (Spec Alignment + Security). |

## Getting Started
### Prerequisites
- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (already included in CI/Docker image)
- Docker (for `make test`)

### Setup
```bash
make setup         # uv sync -> installs dependencies into .venv
make spec-check    # verifies required specs/skills/tests are present
```

### Running Tests
```bash
uv run pytest              # executes intentional failing tests locally
make test                  # builds the Docker image and runs pytest inside it
```
> Tests currently fail by design (`NotImplementedError`) to define the contract boundaries for future agents.

## Developer Workflow
1. **Spec-First** – Never ship code without updating the spec artifacts first. Every feature must trace back to [specs/](specs) and the rules enforced by `.cursor` (TBD) / MCP context.
2. **TDD Guardrails** – Implement code only after the failing suites in [tests/test_trend_fetcher.py](tests/test_trend_fetcher.py) and [tests/test_skills_interface.py](tests/test_skills_interface.py) define success.
3. **Tooling Discipline** – Use MCP servers (git-mcp, filesystem-mcp, weaviate-mcp, coinbase-mcp) for development. Track decisions in [research/tooling_strategy.md](research/tooling_strategy.md).
4. **Skills as Contracts** – All runtime capabilities live under [skills/](skills/README.md) with deterministic JSON envelopes so Planner/Worker/Judge roles stay decoupled from API drift.

## Containerization, CI, and AI Governance
- `Dockerfile` encapsulates the uv-managed environment; caches dependency sync before copying source for faster builds.
- `Makefile` exposes:
	- `make setup` – install deps.
	- `make spec-check` – structural compliance.
	- `make test` – dockerized pytest run.
- GitHub Actions ([.github/workflows/main.yml](.github/workflows/main.yml)) executes the same targets on every push.
- [.coderabbit.yaml](.coderabbit.yaml) configures CodeRabbit to block merges on spec misalignment or security regressions.

## MCP & IDE Context
- [.vscode/mcp.json](.vscode/mcp.json) registers Tenx Feedback Analytics + git-mcp servers so MCP Sense can audit reasoning.
- Future work: finalize `.cursor/rules` / CLAUDE instructions to ensure every IDE co-pilot follows the Prime Directive (“NEVER generate code without checking specs/ first”).

## Roadmap / Next Steps
- Fill in the “empty slots” by implementing the skill interfaces so tests go green.
- Extend [scripts/spec_check.py](scripts/spec_check.py) with semantic diff checks (e.g., ensuring API contracts stay in sync with code).
- Complete the IDE rules file and capture MCP Sense connection logs to finish Task 1.3 requirements.
- Produce the submission assets (research report PDF, Loom walkthrough, MCP telemetry confirmation).

Stay spec-first, keep MCP boundaries clean, and let the swarm scale safely.