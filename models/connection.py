from pydantic import BaseModel, ConfigDict
from starlette.websockets import WebSocket

class Connection(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    socket: WebSocket
    id:int
