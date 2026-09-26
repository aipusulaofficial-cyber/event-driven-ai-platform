from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from broker import InMemoryBroker
from event_domain import Event

app = FastAPI(title="event-driven-ai-platform", version="1.1.0")
broker = InMemoryBroker()\napp.add_middleware(PrincipalObservabilityMiddleware)


class EventPayload(BaseModel):
    topic: str | None = Field(default=None, min_length=1, max_length=128)
    data: dict = Field(default_factory=dict, max_length=32)


class Request(BaseModel):
    key: str = Field(min_length=1, max_length=128)
    payload: EventPayload = Field(default_factory=EventPayload)


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/events")
async def handle(request: Request):
    try:
        event = Event.create(
            request.payload.topic or request.key,
            request.key,
            request.payload.data,
        )
        await broker.publish(event.topic, event.key, request.payload.data)
        return {"event_id": event.event_id, "topic": event.topic, "status": "published"}
    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
