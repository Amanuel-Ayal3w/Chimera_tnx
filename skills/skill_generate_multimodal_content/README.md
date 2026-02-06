# skill_generate_multimodal_content

Transforms a Planner-approved brief into coordinated text, image, and short-form video assets while honoring SOUL.md persona constraints and budget governors.

## MCP Interfaces
- **Resources**: `persona://<agent>/SOUL`, `memory://semantic/<agent>`, `trend://id`
- **Tools**: `generatetext`, `generateimage`, `generatevideo`, `summarize_feedback`

## Input Contract
```json
{
  "version": "1.0",
  "trace_id": "uuid",
  "planner_task_id": "uuid",
  "payload": {
    "campaign_id": "uuid",
    "agent_id": "uuid",
    "persona_profile_ref": "filesystem://agents/<agent>/SOUL.md",
    "trend_context": {
      "trend_id": "uuid",
      "insight_summary": "Upcycled denim + solar charging accessories are spiking in Addis Ababa."
    },
    "artifact_plan": [
      {
        "artifact_id": "uuid",
        "modality": "text",
        "platform": "instagram",
        "length": {"min_tokens": 60, "max_tokens": 120},
        "call_to_action": "Join the #SolarThreads challenge"
      },
      {
        "artifact_id": "uuid",
        "modality": "image",
        "platform": "instagram",
        "style": "vibrant documentary",
        "aspect_ratio": "4:5"
      }
    ],
    "guardrails": {
      "banned_topics": ["politics"],
      "required_tone": "playful" ,
      "max_budget_usd": 0.40
    }
  }
}
```

### Validation Rules
- `artifact_plan` list cannot exceed 5 entries per invocation.
- `max_budget_usd` ensures aggregate model/tool spend stays within Governor limits.
- Each artifact must declare modality-specific constraints (length, style, duration, etc.).

## Output Contract
```json
{
  "version": "1.0",
  "status": "SUCCESS",
  "trace_id": "uuid",
  "payload": {
    "artifacts": [
      {
        "artifact_id": "uuid",
        "modality": "text",
        "platform": "instagram",
        "content": "Solar-powered denim drops in Addis...",
        "tokens_used": 98,
        "safety_score": 0.93,
        "confidence": 0.88,
        "media_uri": null,
        "metadata": {
          "hashtags": ["#SolarThreads", "#AddisFashion"],
          "reading_level": "Grade 8"
        }
      },
      {
        "artifact_id": "uuid",
        "modality": "image",
        "platform": "instagram",
        "content": null,
        "media_uri": "s3://chimera/artifacts/img-bc9f.png",
        "prompt": "Ethiopian model wearing solar denim in sunset bazaar",
        "safety_score": 0.91,
        "confidence": 0.83,
        "metadata": {
          "dimensions": "1080x1350",
          "model_provider": "Gemini-Image-3"
        }
      }
    ],
    "cost_summary_usd": 0.36,
    "latency_ms": 4200
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
    {"code": "GUARDRAIL_VIOLATION", "detail": "Generated copy referenced banned topic"}
  ]
}
```

## Operational Notes
- Workers stream partial tokens; Judges require final consolidated payload.
- Store generated assets in the Artifact Registry (PostgreSQL + object storage) and reference via URI.
- Emit per-artifact telemetry for cost, latency, and safety to feed fleet KPIs.
