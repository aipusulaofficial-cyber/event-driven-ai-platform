from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class Event:
    topic: str
    key: str
    payload: dict
    event_id: str

    def __post_init__(self) -> None:
        if not self.topic.strip() or not self.key.strip():
            raise ValueError("topic and key are required")
        if not self.event_id.strip():
            raise ValueError("event_id is required")

    @classmethod
    def create(cls, topic: str, key: str, payload: dict) -> "Event":
        return cls(topic, key, payload, uuid4().hex)


class IdempotencyStore:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def first_seen(self, event_id: str) -> bool:
        if not event_id.strip():
            raise ValueError("event_id is required")
        if event_id in self._seen:
            return False
        self._seen.add(event_id)
        return True


def retry_delay(attempt: int, base: float = 0.5, cap: float = 30.0) -> float:
    if attempt < 0 or base <= 0 or cap <= 0 or base > cap:
        raise ValueError("invalid retry configuration")
    return min(cap, base * (2**attempt))
