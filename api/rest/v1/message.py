from fastapi import APIRouter, Depends, HTTPException
from Controller.api.websocket import ConnectionManager

router = APIRouter(tags=["test","message"])

@router.get("/message")
async def message(msg:str):
    print(msg)
    await ConnectionManager.manager.broadcast(msg)
    return {"success":True}