from typing import List, Union
from fastapi import WebSocket,status
from Controller.models.message import SubcribeWorker
from Controller.db.schema import SessionLocal
from Controller.services.worker_service import WorkerService
from Controller.models.connection import Connection

def getWorkerService() -> WorkerService: 
    return WorkerService(session=SessionLocal())

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Connection] = []
    
    def search(self,param:Union[WebSocket,int])->Connection|None:
        for connection in self.active_connections:
            if connection.socket == param or connection.id == param:
                return connection

    async def connect(self, websocket: WebSocket, clientInfo:SubcribeWorker):
        service = getWorkerService()
        id = service.create_worker(clientInfo.email).id
        if self.search(id) != None:
            await websocket.accept()
            await websocket.close(code=status.WS_1000_NORMAL_CLOSURE,reason="Already Connected from another isntance")
            return
        self.active_connections.append(Connection(socket=websocket,id=id))
        await websocket.accept()

    def disconnect(self, connectionParam: Union[WebSocket,int]):
        for connection in self.active_connections:
            if connection.socket == connectionParam or connection.id == connectionParam:
                self.active_connections.remove(connection)
    
    async def send(self,connectionParam: Union[WebSocket,int],message:str) -> bool:
        for connection in self.active_connections:
            if connection.socket == connectionParam or connection.id == connectionParam:
                await connection.socket.send_text(message)
                return True
        return False

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.socket.send_text(message)

manager = ConnectionManager()