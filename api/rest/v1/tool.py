from fastapi import APIRouter

router = APIRouter(tags=["ping","control","managment"])

@router.get("/ping")
def ping():
    return {"active":True}