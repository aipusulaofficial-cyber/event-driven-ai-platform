from event_platform import *


def test_idempotency():
    b = EventBus()
    seen = []
    b.subscribe("x", lambda e: seen.append(e.id))
    e = Event("1", "x", {})
    assert b.publish(e) == "processed"
    assert b.publish(e) == "duplicate"
    assert seen == ["1"]


def test_dead_letter_after_bounded_retry():
    b = EventBus(2)
    b.subscribe("x", lambda e: (_ for _ in ()).throw(RuntimeError()))
    assert b.publish(Event("1", "x", {})) == "dead-letter"
    assert len(b.dead_letters) == 1


def test_unhandled_event_is_successful():
    assert EventBus().publish(Event("1", "none", {})) == "processed"
