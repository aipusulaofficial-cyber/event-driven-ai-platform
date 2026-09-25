from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field

from event_domain import Event
from observability import configure_observability, get_logger

configure_observability()
logger = get_logger(__name__)

app = FastAPI(title="event-driven-ai-platform", version="1.0.0")
tracer = trace.get_tracer("event-driven-ai-platform")


class Request(BaseModel):
    key: str
    payload: dict = Field(default_factory=dict)


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/v1/events")
def handle(request: Request) -> dict[str, str]:
    with tracer.start_as_current_span("event-driven-ai-platform.publish"):
        try:
            event = Event.create(
                request.payload.get("topic", request.key),
                request.key,
                request.payload,
            )
            logger.info(
                "event_accepted topic=%s key=%s event_id=%s",
                event.topic,
                event.key,
                event.event_id,
            )
            return {
                "event_id": event.event_id,
                "topic": event.topic,
                "status": "accepted",
            }
        except (ValueError, KeyError, TypeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
