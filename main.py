import base64
import os
import backend.app.db_init


from backend.app.routes import payments, tickets, admin_auth

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.include_router(tickets.router)
app.include_router(payments.router)

app.include_router(admin_auth.router)

ticket_price = os.getenv("TICKET_PRICE")


# Serve frontend
app.mount("/static", StaticFiles(directory="frontend/static", html=True), name="static")

# Jinja2 template configuration
templates = Jinja2Templates(directory="frontend/templates")

templates.env.filters["b64encode"] = lambda s: base64.b64encode(s.encode()).decode()
templates.env.filters["b64decode"] = lambda s: base64.b64decode(s).decode()


# Route for serving the main HTML page
@app.get("/")
async def serve_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "ticket_price": ticket_price})

@app.get("/tickets/scan")
async def scan( request: Request ):
    session_id =  request.cookies.get("session_id")
    if not session_id:
        return templates.TemplateResponse("admin.html", {"request": request})

    from backend.app.services.auth import Auth
    from backend.app.database import get_db

    auth = Auth(get_db())

    user = auth.get_user_from_session_id(session_id)

    if not user:
        return templates.TemplateResponse("admin.html", {"request": request})

    return templates.TemplateResponse("scanner.html", {"request": request})