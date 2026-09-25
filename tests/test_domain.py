import pytest

from event_domain import Event, IdempotencyStore, retry_delay


def test_idempotency_and_backoff():
    store = IdempotencyStore()
    event = Event.create("x", "k", {})
    assert store.first_seen(event.event_id)
    assert not store.first_seen(event.event_id)
    assert retry_delay(3) == 4


def test_event_invariants():
    with pytest.raises(ValueError):
        Event.create("", "k", {})
    with pytest.raises(ValueError):
        IdempotencyStore().first_seen("")
    with pytest.raises(ValueError):
        retry_delay(-1)
    with pytest.raises(ValueError):
        retry_delay(1, base=31, cap=30)
