# Portfolio Evidence

## Executable proof
- Domain evidence verifies event acceptance and duplicate rejection.
- Retry backoff behavior is measured deterministically.
- CI uploads the resulting evidence artifact.

## Architecture proof
Event → idempotency boundary → handler → retry policy → observable outcome.

## Portfolio signal
Event-driven reliability is demonstrated with explicit idempotency and retry evidence.
