from http import HTTPStatus

from fastapi import APIRouter, Depends, Header, HTTPException, Response, Request
from sqlalchemy.orm import Session
from backend.app.schemas import AdminLogin
from backend.app.models import Admin
from backend.app.database import get_db
from backend.app.services.auth import Auth
from datetime import timedelta
import os

router = APIRouter()
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


@router.post("/admin/register")
def register_for_admin(admin: AdminLogin, register_api_key: str = Header(None), db: Session = Depends(get_db)):
    if register_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    auth_service = Auth(db)  # Pass the DB session to AuthService
    try:
        auth_service.register_user(admin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "message": "User registered successfully"
    }, HTTPStatus.CREATED


@router.post("/admin/login")
def login_for_admin(login: AdminLogin, response: Response, db: Session = Depends(get_db)):
    auth_service = Auth(db)
    session = auth_service.valid_login(login)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    response.set_cookie(
        key="session_id",
        value=session,
        httponly=True,  # Prevents JavaScript access (defends against XSS)
        secure=True,  # Use only over HTTPS
        samesite="Strict",  # Prevent CSRF (or "Lax" if you need cross-site POSTs)
        max_age=3600  # Optional: 1 hour expiration
    )
    return {"message": "Login successful"}, HTTPStatus.OK

@router.post("/admin/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    # Get the session ID from the cookies
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID not found in cookies")

    # Authenticate the user (check if the session ID is valid)
    auth_service = Auth(db)
    auth_service.destroy_session(session_id)

    response.delete_cookie(key="session_id")

    return {"message": "Logout successful"}, HTTPStatus.OK
