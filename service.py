from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from event_domain import *
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"event-driven-ai-platform"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="event-driven-ai-platform",version="1.0.0");tracer=trace.get_tracer("event-driven-ai-platform")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/events")
def handle(r:Request):
 with tracer.start_as_current_span("event-driven-ai-platform.domain"):
  try: e=Event.create(r.payload.get("topic",r.key),r.key,r.payload);return {"event_id":e.event_id,"topic":e.topic,"status":"accepted"}
  except (ValueError,KeyError,RuntimeError) as e: raise HTTPException(status_code=400,detail=str(e)) from e
