# Event-Driven AI Platform

An asynchronous AI platform built around explicit event contracts, idempotent processing, failure isolation and observable execution.

## Event lifecycle
```text
producer -> event contract -> consumer -> domain handler -> side effect -> acknowledgement
                                  |
                             retry / dead-letter policy
```

## Contracts
- Event shape and version are explicit.
- Consumers validate before processing.
- Processing is designed to be idempotent where retries can occur.
- Acknowledgement follows the defined processing boundary.
- Failure and retry semantics are visible rather than implicit.

## Reliability
Transient dependency failures can be retried within bounded policy. Permanent failures are isolated instead of causing an entire stream to appear successful.

## Observability & security
Correlation context follows events through processing. Least-privilege controls and input validation protect asynchronous boundaries.

## Verification
Contract, edge-case and failure-path tests are part of CI, with production and security validation as delivery gates.

## Evidence
[ARCHITECTURE.md](ARCHITECTURE.md) · [docs/PRINCIPAL-ENGINEERING.md](docs/PRINCIPAL-ENGINEERING.md) · [ADRs](ADRs/)