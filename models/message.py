from pydantic import BaseModel

class MessageSend(BaseModel):
    message:str

class SubcribeWorker(BaseModel):
    email:str