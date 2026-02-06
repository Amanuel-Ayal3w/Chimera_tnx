# Project Chimera Skill Packages

Project Chimera exposes every agent capability as a standalone MCP-compatible "skill" package so the Planner/Worker/Judge swarm can compose actions safely. Each skill wraps an external system (news APIs, foundation models, publishing endpoints, etc.) behind a consistent JSON contract so the agents stay decoupled from API churn.

## Skill Index
| Skill | Purpose | Primary MCP Resources & Tools | Contracts |
| --- | --- | --- | --- |
| [skill_fetch_trends](skill_fetch_trends/README.md) | Harvest macro/micro trends from news, social, and commerce feeds to seed campaigns. | `news://`, `social://mentions`, `commerce://sales`, tools: `fetchtrends`, `search_memory`. | Inputs: `platform`, `topics`, `time_window`. Outputs: normalized `trends[]` with scores + citations. |
| [skill_generate_multimodal_content](skill_generate_multimodal_content/README.md) | Produce long-form copy plus optional image/video assets aligned with persona goals. | Tools: `generatetext`, `generateimage`, `generatevideo`, resources: `persona://SOUL`, `memory://semantic`. | Inputs: `campaign_context`, `artifact_plan`. Outputs: `artifacts[]` each with modality, URI, confidence. |
| [skill_validate_content](skill_validate_content/README.md) | Apply automated guardrails before Judge/HITL review, checking policy, brand, and safety. | Tools: `validatecontent`, `classify_sentiment`, resources: `policies://brand`, `risk://keywords`. | Inputs: `artifact`, `policy_bundle`, `delivery_target`. Outputs: `status`, `violations`, `recommended_actions`. |

## Contract Conventions
- **Traceability**: Every request/response carries `trace_id` and `planner_task_id` so telemetry can stitch Planner→Worker→Judge hops.
- **Deterministic envelopes**: Inputs and outputs are wrapped in `{ "version": "1.0", "payload": { ... } }` to allow additive evolution without breaking callers.
- **Confidence-first**: All outputs include a `confidence` float plus optional `evidence` array for judges/HITL reviewers.
- **Error surfaces**: Skills never throw opaque errors. They return `{ "status": "ERROR", "errors": [ { "code": "DOWNSTREAM_TIMEOUT", ... } ] }` so the Planner can re-plan.

See each skill README for detailed field definitions, validation rules, and example transactions.
