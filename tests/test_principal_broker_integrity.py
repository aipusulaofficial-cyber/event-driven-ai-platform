import asyncio

import pytest

from broker import InMemoryBroker


def test_published_event_is_immutable_snapshot():
    broker = InMemoryBroker()
    payload = {"nested": {"value": 1}}
    assert asyncio.run(broker.publish("topic", "id-1", payload)) == "id-1"
    payload["nested"]["value"] = 2
    assert broker.messages == [("topic", "id-1", {"nested": {"value": 1}})]


@pytest.mark.parametrize(
    "topic,key,payload",
    [("", "id", {}), ("topic", "", {}), ("topic", "id", None)],
)
def test_invalid_event_rejected(topic, key, payload):
    broker = InMemoryBroker()
    with pytest.raises(ValueError):
        asyncio.run(broker.publish(topic, key, payload))
    assert broker.messages == []
