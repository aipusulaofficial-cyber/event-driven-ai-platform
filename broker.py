from typing import Protocol


class EventBroker(Protocol):
    async def publish(self, topic:str, key:str, payload:dict)->str: ...


class InMemoryBroker:
    def __init__(self): self.messages=[]
    async def publish(self,topic,key,payload):
        self.messages.append((topic,key,payload)); return key
