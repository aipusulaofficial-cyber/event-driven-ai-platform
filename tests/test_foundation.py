from event_domain import Event, IdempotencyStore, retry_delay


def test_event_contract_and_idempotency():
    event = Event.create("orders", "order-1", {"amount": 10})
    assert event.topic == "orders"
    assert event.key == "order-1"
    store = IdempotencyStore()
    assert store.first_seen(event.event_id) is True
    assert store.first_seen(event.event_id) is False


def test_retry_delay_is_bounded():
    assert retry_delay(0) == 0.5
    assert retry_delay(10) == 30.0
