from typing import List, Union
from fastapi import WebSocket
from Controller.models.message import SubcribeWorker
from Controller.db.schema import SessionLocal
from Controller.services.worker_service import WorkerService
from Controller.models.connection import Connection

def getWorkerService() -> WorkerService: 
    return WorkerService(session=SessionLocal())

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Connection] = []

    async def connect(self, websocket: WebSocket, clientInfo:SubcribeWorker):
        await websocket.accept()
        service = getWorkerService()
        id = service.create_worker(clientInfo.email).id
        self.active_connections.append(Connection(socket=websocket,id=id))

    def disconnect(self, connectionParam: Union[WebSocket,int]):
        for connection in self.active_connections:
            if connection.socket == connectionParam or connection.id == connectionParam:
                self.active_connections.remove(connection)
    
    async def send(self,connectionParam: Union[WebSocket,int],message:str):
        for connection in self.active_connections:
            if connection.socket == connectionParam or connection.id == connectionParam:
                await connection.socket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.socket.send_text(message)

manager = ConnectionManager()