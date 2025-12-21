
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Controller.core.config import config
from Controller.core.startup import initialize
from Controller.core.logging import setup_logging
from Controller.db.schema import Base, engine
from Controller.api.websocket.v1 import worker
from Controller.api.rest.v1 import message
from Controller.frontend.ui import ui

setup_logging()
Base.metadata.create_all(bind=engine)

if not initialize():
    print("cannot connect to internet")

app = FastAPI(title=config.app_name)

app.include_router(worker.router,prefix="/network/v1")
app.include_router(message.router,prefix="/api/v1/message")

# app.mount("/", StaticFiles(directory="Controller/static", html=True), name="static")

ui.run_with(
    app=app,
    # storage_secret='your private secret', # Required for user storage, dark mode persistence, etc.
    title="Test App",
    favicon="client.png"
)