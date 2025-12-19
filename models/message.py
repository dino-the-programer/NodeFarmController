from pydantic import BaseModel

class MessageSend(BaseModel):
    message:str
    id:str|None=None
    email:str|None=None

class SubcribeWorker(BaseModel):
    email:str