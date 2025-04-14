from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from backend.app.routes import payments, tickets
import backend.app.db_init

app = FastAPI()

app.include_router(tickets.router)
app.include_router(payments.router)


# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
