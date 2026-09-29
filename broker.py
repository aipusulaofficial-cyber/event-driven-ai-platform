from copy import deepcopy
from typing import Protocol


class EventBroker(Protocol):
    async def publish(self, topic: str, key: str, payload: dict) -> str: ...


class InMemoryBroker:
    """Single-process broker used for deterministic local tests, not durable delivery."""

    def __init__(self):
        self.messages = []

    async def publish(self, topic, key, payload):
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic is required")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("message key is required")
        if not isinstance(payload, dict):
            raise ValueError("event payload must be a dictionary")
        # Isolate published events from caller mutations after admission.
        self.messages.append((topic, key, deepcopy(payload)))
        return key
