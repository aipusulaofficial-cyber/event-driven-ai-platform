"""Event-driven AI core with idempotency, bounded retries and dead-letter handling."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Event: id:str; type:str; payload:dict
class EventBus:
 def __init__(self,max_retries=2):self.max_retries=max_retries;self.handlers={};self.processed=set();self.dead_letters=[]
 def subscribe(self,t,h):self.handlers.setdefault(t,[]).append(h)
 def publish(self,e):
  if e.id in self.processed:return "duplicate"
  failures=0
  for h in self.handlers.get(e.type,[]):
   while True:
    try:h(e);break
    except Exception:
     failures+=1
     if failures>self.max_retries:self.dead_letters.append(e);return "dead-letter"
  self.processed.add(e.id);return "processed"
