from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.app.routes import payments, tickets, admin_auth
import backend.app.db_init
import os

app = FastAPI()

app.include_router(tickets.router)
app.include_router(payments.router)

app.include_router(admin_auth.router)

ticket_price = os.getenv("TICKET_PRICE")


# Serve frontend
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")

# Jinja2 template configuration
templates = Jinja2Templates(directory="frontend/templates")

# Route for serving the main HTML page
@app.get("/")
async def serve_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "ticket_price": ticket_price})