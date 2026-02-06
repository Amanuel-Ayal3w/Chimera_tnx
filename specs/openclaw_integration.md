# OpenClaw Integration Plan – Availability & Status Broadcasting

## 1. Purpose
Define how Project Chimera agents announce operational availability, persona status, and commerce readiness to the OpenClaw network while adhering to FastRender swarm governance, MCP-only interfaces, and security expectations derived from the OpenClaw/MoltBook research notes.

## 2. Background Signals
- **OpenClaw** provides a federated agent social graph where agents exchange signed status beacons, advertise capabilities, and discover peer services. Research indicates 22–26% of community skills were vulnerable, demanding audited skill pipelines and strict contract validation.
- **MoltBook** demonstrates emergent agent-only social networks where autonomous posting can create opaque behavior. Publishing availability into OpenClaw must therefore include persona provenance, confidence metrics, and revocation hooks.

## 3. Integration Objectives
1. **Transparent Presence** – Communicate when each Chimera agent is online, idle, or engaged, including campaign focus and wallet governance tier.
2. **Safety Boundaries** – Ensure every broadcast references Judge confidence and persona SLAs to avoid rogue agents misrepresenting capabilities.
3. **Discovery & Scheduling** – Allow external OpenClaw coordinators to request collaborations (e.g., cross-promotions) through a controlled queue that respects Planner tasking and governor limits.
4. **Revocation & Incident Response** – Provide immediate quarantine signals if an agent is paused, compromised, or under human review.

## 4. Status Taxonomy
| Field | Description |
| --- | --- |
| `agent_id` | UUID matching `agents.agent_id` |
| `persona_slug` | SOUL.md slug for public reference |
| `presence_state` | `ONLINE`, `IDLE`, `BUSY`, `OFFLINE`, `QUARANTINED` |
| `campaign_focus` | High-level OKR tag (e.g., `launch_fashion_drop`) |
| `confidence_window` | Rolling average Judge confidence (0–1) |
| `wallet_band` | `LOW_SPEND`, `STANDARD`, `HIGH_SPEND` based on governor limits |
| `hitl_queue_depth` | Count of pending HITL items influencing responsiveness |
| `signature` | Ed25519 or secp256k1 signature using AgentKit key |

## 5. MCP Interface Design
- **MCP Server**: `mcp-server-openclaw` (new) exposing:
  - `status.publish_availability` – Push current status beacon (JSON above) to OpenClaw gateway.
  - `status.revoke` – Broadcast emergency OFFLINE/QUARANTINED state.
  - `status.fetch_neighbors` – (Optional) Retrieve allied agent statuses for Planner situational awareness.
- **Transport**: SSE/WebSocket to OpenClaw aggregator with TLS + mutual attestation.
- **Contracts**: JSON schema stored under `specs/contracts/openclaw-status.json` (to be created during planning) with versioning tied to `protocol_version` field.

## 6. Workflow
1. **Planner Trigger** – Every time a Planner commits a new DAG root or detects major state drift, it emits `STATUS_UPDATE` task.
2. **Worker Execution** – Dedicated Worker aggregates telemetry: queue depth, wallet limits, persona slug, Judge rolling confidence.
3. **Judge Validation** – Judge verifies data freshness (<5s), ensures signature nonce is unused, and checks that presence change respects governance (e.g., cannot advertise `BUSY` if agent is quarantined).
4. **Broadcast** – Worker invokes `status.publish_availability`; OpenClaw network acknowledges with `trace_id` logged to PostgreSQL `openclaw_status_log` table.
5. **External Requests** – OpenClaw peers submit collaboration intents via `status_request` channel; Planner ingests as tasks only after CFO confirms budget capacity.
6. **Revocation Path** – If Judge or Operator pauses an agent, `status.revoke` runs immediately, forcing `QUARANTINED` state and notifying OpenClaw watchers.

## 7. Data Persistence
Create table `openclaw_status_log`:
```
status_id UUID PRIMARY KEY
agent_id UUID REFERENCES agents(agent_id)
payload JSONB
ack_trace_id VARCHAR(64)
state_version BIGINT
broadcast_at TIMESTAMP DEFAULT NOW()
ack_latency_ms INT
```
This supports auditing, replay, and anomaly detection when OpenClaw responses lag.

## 8. Security & Compliance
- **Signed Payloads**: All broadcasts signed with AgentKit wallet keys; signatures verified server-side before external publish.
- **Rate Limiting**: Default 1 update per minute per agent; bursts allowed during incident response.
- **Quarantine Hooks**: If OpenClaw reports compromised credentials, CFO Judge freezes commerce actions and Operators must rotate keys before resuming broadcasts.
- **Skill Supply Chain**: Only signed skills can run the OpenClaw MCP server; CI must scan dependencies per the 22–26% exploit finding.

## 9. Implementation Roadmap
1. **Spec Alignment** – Finalize JSON schema + contract tests referencing technical spec (tasks, ledger, persona data). Update `/speckit.plan` to include the new MCP server.
2. **Server Build** – Implement `mcp-server-openclaw` with publish/revoke APIs, including signature middleware and retry logic.
3. **Telemetry Collector** – Extend Planner telemetry service to compute `confidence_window`, `hitl_queue_depth`, and wallet bands.
4. **Judge Policy** – Add constitution-backed check ensuring no broadcast occurs without fresh Judge approval.
5. **Incident Playbooks** – Document Operator steps for manual overrides, key rotation, and MoltBook-style emergent monitoring.

## 10. Risks & Mitigations
- **Spoofed Status Messages** → mitigate via cryptographic signatures and OpenClaw mutual attestation.
- **Information Leakage** → only expose high-level campaign tags; never share internal prompts, user data, or wallet balances.
- **Availability Storms** → throttle incoming collaboration intents, queue them through Planner with budget checks.
- **Emergent Behavior** → log every broadcast with trace IDs so Operators can correlate unusual OpenClaw interactions with internal events.
