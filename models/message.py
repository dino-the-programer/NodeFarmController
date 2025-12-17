from pydantic import BaseModel

class MessageSend(BaseModel):
    message:str