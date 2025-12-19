from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Controller.db.schema import Worker

class WorkerService:
    def __init__(self, session:Session) -> None:
        self._db = session
    
    def list_workers(self) -> list[Worker]:
        return self._db.query(Worker).all()
    
    def query_worker(self, worker_id:int|None=None, email:str|None=None) -> Worker|None:
        return self._db.query(Worker).filter(or_(Worker.id == worker_id, Worker.email==email)).first()
    
    def create_worker(self, email:str) -> Worker:
        worker = self.query_worker(email=email)
        if worker!=None:
            return worker
        worker = Worker(email = email)
        self._db.add(worker)
        self._db.commit()
        self._db.refresh(worker)
        return worker