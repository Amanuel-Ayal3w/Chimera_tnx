# skill_fetch_trends

Harvests trend intelligence for the Planner. Workers invoke this skill to consolidate cultural, news, and commerce signals into a normalized payload that downstream content generation can trust.

## MCP Interfaces
- **Resources**: `news://<region>/<topic>`, `social://platform/<handle>/mentions`, `commerce://sku/<id>/velocity`
- **Tools**: `fetchtrends` (primary), `search_memory` (fallback for historical context)

## Input Contract
```json
{
  "version": "1.0",
  "trace_id": "uuid",
  "planner_task_id": "uuid",
  "payload": {
    "platform": "twitter | instagram | tiktok | youtube | global",
    "topics": ["summer fashion", "ethiopia"],
    "time_window": {
      "start": "2026-02-01T00:00:00Z",
      "end": "2026-02-06T00:00:00Z"
    },
    "signals": {
      "include_news": true,
      "include_social": true,
      "include_commerce": false
    },
    "geo": "global | iso-3166-1 code",
    "persona_priority": ["eco-conscious", "gen-z"]
  }
}
```

### Validation Rules
- `platform` must map to an enabled MCP server; `global` aggregates all.
- `time_window` range \<= 7 days to control API cost.
- At least one of news/social/commerce signals must be true.

## Output Contract
```json
{
  "version": "1.0",
  "status": "SUCCESS",
  "trace_id": "uuid",
  "payload": {
    "trends": [
      {
        "trend_id": "uuid",
        "platform": "twitter",
        "topic": "#SolarFashion",
        "momentum_score": 0.82,
        "volume": 15432,
        "sentiment": 0.66,
        "summary": "Designers pairing solar fabrics with traditional Ethiopian patterns.",
        "source_citations": [
          {
            "type": "tweet",
            "url": "https://twitter.com/...",
            "captured_at": "2026-02-05T10:02:00Z"
          }
        ]
      }
    ],
    "embeddings_ref": "weaviate://collections/trends/record-uuid",
    "confidence": 0.9
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
    {"code": "RATE_LIMIT", "detail": "Twitter API bucket exhausted", "retry_after_seconds": 900}
  ]
}
```

## Operational Notes
- Persist `trends` objects to PostgreSQL (`trends` table) and pgvector for similarity recall.
- Emit telemetry counters per platform to track coverage and hit rate.
- Planner retries up to 2x with backoff; on repeated failure, fallback to cached embeddings.
