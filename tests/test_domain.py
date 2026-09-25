from event_domain import *
def test_idempotency_and_backoff():
 s=IdempotencyStore();e=Event.create("x","k",{});assert s.first_seen(e.event_id);assert not s.first_seen(e.event_id);assert retry_delay(3)==4