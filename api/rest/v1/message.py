from fastapi import APIRouter, Depends, HTTPException
from Controller.api.websocket import connection

router = APIRouter(tags=["test","message"])

router.get("/{msg}")
async def message(msg:str):
    await connection.manager.broadcast(msg)
    return {"success":True}