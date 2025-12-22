from typing import List, Union
from fastapi import WebSocket,status
from Controller.models.message import SubcribeWorker
from Controller.db.schema import SessionLocal
from Controller.services.worker_service import WorkerService
from Controller.models.connection import Connection
from Controller.frontend.admindashboard import workerListUI, worker_list_ui


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
        workerListUI.update({id:clientInfo.email})
        worker_list_ui.refresh()
        await websocket.accept()

    def disconnect(self, connectionParam: Union[WebSocket, int]):
    # Find the specific connection
        connection_to_remove = None
        for connection in self.active_connections:
            if connection.socket == connectionParam or connection.id == connectionParam:
                connection_to_remove = connection
                break
        if connection_to_remove:
            self.active_connections.remove(connection_to_remove)
            workerListUI.pop(connection_to_remove.id)
            worker_list_ui.refresh()
    
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