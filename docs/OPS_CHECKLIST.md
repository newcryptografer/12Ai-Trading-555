# Ops Checklist

- MODE defaults to paper.
- Use WebSocket first, REST only for bootstrap and low-frequency endpoints.
- Respect WebSocket and REST shared rate limits.
- Reconnect on disconnect and re-subscribe.
- Order user-data messages by event time E.
- Cap risk per trade, daily loss, open risk, and correlation.
- Use circuit breaker on repeated failures.
- Run health checks for data freshness, stream status, and order status.
- Keep ensemble feature cache per interval.
- Compute indicators once per candle batch.
