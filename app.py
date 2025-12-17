from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Controller.core.config import config
from Controller.core.logging import setup_logging
from Controller.db.schema import Base, engine
from Controller.comms import publisher, tunnel

setup_logging()
Base.metadata.create_all(bind=engine)
tunnelUrl = tunnel.Tunnel.CreateTunnel(os.getenv("PINGGY_TOKEN"))
publisher.publish(os.getenv("GITHUB_TOKEN"),publisher.DomainEndPoint(url=tunnelUrl,active=True))

app = FastAPI(title=config.app_name)
app.mount("/", StaticFiles(directory="Controller/static", html=True), name="static")

