from copy import deepcopy
from typing import Protocol


class EventBroker(Protocol):
    async def publish(self, topic: str, key: str, payload: dict) -> str: ...


class InMemoryBroker:
    def __init__(self):
        self.messages = []

    async def publish(self, topic, key, payload):
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic is required")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("event key is required")
        if not isinstance(payload, dict):
            raise ValueError("payload must be a mapping")
        self.messages.append((topic, key, deepcopy(payload)))
        return key
