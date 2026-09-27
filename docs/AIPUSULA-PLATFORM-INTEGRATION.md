# AIPusula Platform Integration — Event Contracts

Events carry correlation ID, schema version, producer, timestamp and idempotency key. Consumers must handle retries and duplicate delivery safely. Policy, audit and observability context propagate with the event.

Engineering standard: Code -> Contract -> Test -> Security -> Runtime -> Observability -> Deployment -> Evidence
