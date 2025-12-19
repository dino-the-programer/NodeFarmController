from fastapi import APIRouter, Depends, HTTPException
from Controller.api.websocket import ConnectionManager
from Controller.models.message import MessageSend
from Controller.db.schema import SessionLocal
from Controller.services.worker_service import WorkerService

def getWorkerService() -> WorkerService: 
    return WorkerService(session=SessionLocal())

router = APIRouter(tags=["test","message"])

@router.get("/broadcast")
async def broadcast(msg:str):
    print(msg)
    await ConnectionManager.manager.broadcast(msg)
    return {"success":True}

@router.post("/send")
async def send(payload:MessageSend):
    if payload.email == None and payload.id == None:
        raise HTTPException(400,f"please provide either email or id")
    service = getWorkerService()
    worker = service.query_worker(email=payload.email)
    if worker==None:
        raise HTTPException(404,f"Email{payload.email} doesnot exist")
    if not await ConnectionManager.manager.send(worker.id,payload.message):
        return {"sucess":False}
    return {"success":True}