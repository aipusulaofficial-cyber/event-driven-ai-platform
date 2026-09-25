from dataclasses import dataclass
from uuid import uuid4

@dataclass(frozen=True)
class Event:
    topic:str; key:str; payload:dict; event_id:str
    @classmethod
    def create(cls,topic,key,payload): return cls(topic,key,payload,uuid4().hex)

class IdempotencyStore:
    def __init__(self): self._seen=set()
    def first_seen(self,event_id:str)->bool:
        if event_id in self._seen:return False
        self._seen.add(event_id);return True

def retry_delay(attempt:int,base:float=0.5,cap:float=30)->float:
    if attempt<0: raise ValueError("negative attempt")
    return min(cap,base*(2**attempt))
