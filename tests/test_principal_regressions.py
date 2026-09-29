import pytest

from broker import InMemoryBroker


@pytest.mark.asyncio
async def test_broker_snapshots_event_payload():
    broker = InMemoryBroker()
    payload = {"nested": {"value": 1}}
    await broker.publish("topic", "key", payload)
    payload["nested"]["value"] = 2
    assert broker.messages[0][2] == {"nested": {"value": 1}}


@pytest.mark.asyncio
async def test_broker_rejects_empty_topic():
    broker = InMemoryBroker()
    with pytest.raises(ValueError):
        await broker.publish("", "key", {})
