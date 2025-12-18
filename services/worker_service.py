from sqlalchemy.orm import Session
from Controller.db.schema import Worker

class WorkerService:
    def __init__(self, session:Session) -> None:
        self._db = session
    
    def list_workers(self) -> list[Worker]:
        return self._db.query(Worker).all()
    
    def query_worker(self, worker_id:int) -> Worker|None:
        return self._db.query(Worker).filter(Worker.id == worker_id).first()
    
    def create_worker(self, email:str) -> Worker:
        worker = Worker(email = email)
        self._db.add(worker)
        self._db.commit()
        self._db.refresh(worker)
        return worker