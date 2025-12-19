from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from Controller.api.websocket.ConnectionManager import manager
from Controller.models.message import SubcribeWorker
from Controller.services.worker_service import WorkerService

router = APIRouter(tags=["message", "network"])

@router.websocket("/subscribe/{email}")
async def websocket_endpoint(websocket: WebSocket, email:str):
    await manager.connect(websocket,SubcribeWorker(email=email))
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send(websocket,f"ping: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError:
        print("Connection not accepted")
