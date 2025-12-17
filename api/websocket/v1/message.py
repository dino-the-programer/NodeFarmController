from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from Controller.api.websocket import connection

router = APIRouter(tags=["message", "network"])

@router.websocket("/subscribe")
async def chat_endpoint(websocket: WebSocket):
    await connection.manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection.manager.broadcast(f"Broadcast: {data}")
    except WebSocketDisconnect:
        connection.manager.disconnect(websocket)