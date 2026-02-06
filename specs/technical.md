# Technical Specification – Project Chimera

## Overview
Project Chimera uses a FastRender Planner→Worker→Judge swarm coordinated through MCP-standardized integrations. PostgreSQL + pgvector anchor transactional/embeddings data, Redis handles coordination, Weaviate stores semantic memory, and Coinbase AgentKit provides non-custodial wallets. This document defines the core contracts shared across services.

## API Contracts
### 1. Planner → Worker Task Contract
```json
{
  "task_id": "uuid-v4",
  "task_type": "generate_content | reply_comment | trend_analysis | execute_transaction",
  "priority": "high | medium | low",
  "context": {
    "goal_description": "string",
    "persona_constraints": ["string"],
    "required_resources": ["mcp://resource/identifier"],
    "budget_cap_usd": 25.0,
    "lock_character_reference": "agent-style-id"
  },
  "payload": {
    "channel": "twitter | instagram | tiktok | blog",
    "trend_reference_id": "uuid-v4",
    "media_requirements": {
      "modalities": ["text", "image", "video"],
      "duration_seconds": 30
    }
  },
  "created_at": "2026-02-06T12:00:00Z",
  "state_version": 128
}
```
- `state_version` enables Judges to enforce optimistic concurrency.
- `lock_character_reference` enforces visual consistency across image/video tools.

### 2. Worker → Judge Result Contract
```json
{
  "task_id": "uuid-v4",
  "worker_id": "worker-instance-id",
  "artifact": {
    "content_type": "social_post | comment_reply | video_story | transaction",
    "text": "string",
    "media_urls": ["https://cdn.chimera.ai/artifacts/img001.png"],
    "tool_execution_logs": [
      {
        "tool": "mcp://ideogram/generate_image",
        "status": "SUCCESS",
        "latency_ms": 2300
      }
    ]
  },
  "confidence_score": 0.84,
  "sensitive_topics": ["financial"],
  "costs": {
    "inference_usd": 1.25,
    "media_generation_usd": 2.10
  },
  "started_at": "2026-02-06T12:01:03Z",
  "completed_at": "2026-02-06T12:01:10Z"
}
```
- Judges route artifacts to HITL when `confidence_score < 0.90` or `sensitive_topics` is non-empty.

### 3. Judge Decision Contract
```json
{
  "task_id": "uuid-v4",
  "decision": "APPROVE | REJECT | HITL_QUEUE",
  "confidence_score": 0.84,
  "state_version": 128,
  "reasoning_trace": "LLM chain-of-thought summary",
  "hitl_ticket_id": "optional-uuid",
  "persona_score": 0.92,
  "safety_flags": {
    "nsfw": false,
    "politics": true
  },
  "next_action": "publish | replan | wait_hitl",
  "logged_at": "2026-02-06T12:01:11Z"
}
```

### 4. Agent Communication Protocol (Handoff)
```json
{
  "protocol_version": "1.2.0",
  "trace_id": "uuid-v4",
  "handoff_context": {
    "source_agent": "worker-42",
    "target_role": "judge-safety",
    "timestamp": "2026-02-06T12:01:05Z"
  },
  "artifact": {
    "content_type": "social_post",
    "platform": "twitter",
    "raw_text": "Generating content based on current trends...",
    "media_urls": ["https://storage.chimera.ai/tmp/img_01.png"]
  },
  "confidence_metrics": {
    "llm_self_score": 0.89,
    "tool_execution_status": "SUCCESS"
  }
}
```

### 5. Commerce Action Request (Worker → CFO Judge)
```json
{
  "request_id": "uuid-v4",
  "agent_id": "uuid-v4",
  "action_type": "native_transfer | deploy_token | get_balance",
  "amount_usdc": 25.0,
  "to_address": "0xabc...",
  "memo": "Pay freelance video editor",
  "risk_score": 0.18,
  "current_daily_spend": 32.0,
  "limits": {
    "max_daily_spend": 50.0,
    "max_transaction_usdc": 30.0
  }
}
```
- CFO Judge rejects requests that violate limits or exceed anomaly thresholds.

## Data Schema (PostgreSQL + pgvector)
### 1. `agents`
```
agent_id UUID PRIMARY KEY
name VARCHAR(255) NOT NULL
persona_slug VARCHAR(100) UNIQUE
wallet_address VARCHAR(42) UNIQUE
soul_config JSONB NOT NULL
governor_limits JSONB DEFAULT '{"max_daily_spend":50,"max_tasks_per_hour":10}'
created_at TIMESTAMP DEFAULT NOW()
updated_at TIMESTAMP DEFAULT NOW()
```

### 2. `tasks`
```
task_id UUID PRIMARY KEY
parent_task_id UUID REFERENCES tasks(task_id)
agent_id UUID REFERENCES agents(agent_id)
task_type VARCHAR(100)
status VARCHAR(50) CHECK (status IN ('PENDING','EXECUTING','JUDGE_REVIEW','HIT_QUEUE','PUBLISHED','FAILED'))
payload JSONB
result_artifact JSONB
confidence_score NUMERIC(3,2)
state_version BIGINT DEFAULT 0
updated_at TIMESTAMP DEFAULT NOW()
```

### 3. `agent_memories`
```
memory_id SERIAL PRIMARY KEY
agent_id UUID REFERENCES agents(agent_id)
content TEXT
embedding VECTOR(1536)
metadata JSONB
created_at TIMESTAMP DEFAULT NOW()
```

### 4. `agent_videos` (Video Metadata Store)
```
video_id UUID PRIMARY KEY
agent_id UUID REFERENCES agents(agent_id)
platform VARCHAR(50)
caption TEXT
character_reference_id VARCHAR(100)
style_preset VARCHAR(100)
duration_seconds INT
render_tier VARCHAR(20) CHECK (render_tier IN ('daily','hero'))
confidence_score NUMERIC(3,2)
media_url TEXT
transcript TEXT
embedding VECTOR(1536)
created_at TIMESTAMP DEFAULT NOW()
```
- `render_tier` captures the Tier 1 vs. Tier 2 strategy.
- `embedding` supports semantic search of video assets.

### 5. `wallet_ledger`
```
entry_id UUID PRIMARY KEY
agent_id UUID REFERENCES agents(agent_id)
tx_hash VARCHAR(80) UNIQUE
action_type VARCHAR(50)
amount_usdc NUMERIC(12,2)
counterparty VARCHAR(255)
status VARCHAR(30) CHECK (status IN ('PENDING','SETTLED','FAILED'))
metadata JSONB
occurred_at TIMESTAMP
recorded_at TIMESTAMP DEFAULT NOW()
```

## Redis Structures
- `task_queue`: List storing serialized Planner tasks (JSON contract #1).
- `review_queue`: List storing Worker results awaiting Judge (contract #2).
- `daily_spend:<agent_id>`: Numeric key tracking cumulative spend; reset via cron.

## Observability Requirements
- Trace IDs propagate through Planner→Worker→Judge→HITL to enable replay.
- Structured logs include `agent_id`, `task_id`, `confidence_score`, and `mcp_server` per action.
- Metrics: queue depth, HITL SLA, spend utilization, MCP error rates.

## Security & Compliance
- Secrets (wallet keys, API tokens) stored in managed services (AWS Secrets Manager/Vault); injected at runtime.
- Skill bundles must be signed and scanned before Workers can download them.
- Automated AI disclosure flags and persona honesty directives enforced at publish time.
