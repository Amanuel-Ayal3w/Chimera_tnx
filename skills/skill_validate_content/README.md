# skill_validate_content

Applies automated compliance, brand, and risk checks before the Judge/HITL phase. This keeps the swarm aligned with persona guardrails, regional regulations, and platform rules.

## MCP Interfaces
- **Resources**: `policies://brand/<tenant>`, `risk://keywords`, `persona://SOUL`
- **Tools**: `validatecontent`, `classify_sentiment`, `detect_entities`

## Input Contract
```json
{
  "version": "1.0",
  "trace_id": "uuid",
  "planner_task_id": "uuid",
  "payload": {
    "artifact": {
      "artifact_id": "uuid",
      "modality": "text | image | video",
      "platform": "instagram",
      "content": "...",
      "media_uri": "optional"
    },
    "policy_bundle": {
      "brand_voice_ref": "filesystem://policies/brand/aiqem.md",
      "regulatory_refs": ["compliance://eu-ai-act/disclosure"],
      "platform_rules": ["platform://instagram/2026-01/publish"]
    },
    "delivery_target": {
      "geo": "ET",
      "audience_segment": "gen-z",
      "release_window": "2026-02-07T09:00:00Z"
    },
    "risk_toggles": {
      "require_disclosure": true,
      "max_negative_sentiment": 0.3,
      "require_wallet_callout": false
    }
  }
}
```

### Validation Rules
- At least one policy document must be provided.
- `artifact.content` is required for text modality; `media_uri` required for image/video.
- Release window must be in the future to avoid stale validations.

## Output Contract
```json
{
  "version": "1.0",
  "status": "SUCCESS",
  "trace_id": "uuid",
  "payload": {
    "validation_result": "APPROVED | NEEDS_REVIEW | REJECTED",
    "confidence": 0.87,
    "violations": [
      {
        "code": "TONE_MISMATCH",
        "severity": "MEDIUM",
        "detail": "Copy leans sarcastic; persona requires playful",
        "evidence": "sentence 2"
      }
    ],
    "recommended_actions": [
      {
        "action": "soften_language",
        "instructions": "Replace 'brag' with 'share'"
      }
    ],
    "disclosure_block": "This post was crafted by Chimera Agent Liyu."
  }
}
```

### Error Envelope
```json
{
  "version": "1.0",
  "status": "ERROR",
  "trace_id": "uuid",
  "errors": [
    {"code": "POLICY_NOT_FOUND", "detail": "Brand policy reference missing"}
  ]
}
```

## Operational Notes
- Results feed the Judge's OCC commit check and determine HITL routing thresholds.
- Persist violation history for auditors and to fine-tune future guardrails.
- If `validation_result` = `NEEDS_REVIEW`, automatically create a HITL queue entry with the payload attached.
