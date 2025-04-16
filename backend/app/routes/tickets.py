import os

from backend.app.database import get_db
from backend.app.models import User, Ticket
from backend.app.services.auth import Auth
from backend.app.services.ticket_delivery import deliver_ticket
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

router = APIRouter()
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
TICKET_GATE_PRICE = int(os.getenv("TICKET_GATE_PRICE"))


@router.post("/tickets/generate")
def generate_ticket_admin(
    body: dict,
    req: Request,
    db: Session = Depends(get_db)
):
    # Get the session ID from the cookies
    session_id = req.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID not found in cookies")

    auth_service = Auth(db)
    admin = auth_service.get_user_from_session_id(session_id).decode('utf-8')


    from backend.app.services.ticket_controller import issue_tickets

    email = body.get('email')  # Get email from the body
    quantity = body.get('quantity', 1)
    phone = body.get('phone', "0")
    name = body.get('name', "")


    tickets = issue_tickets(
        db=db,
        email=email,
        quantity=quantity,
        name=name,
        phone=phone,
        payment_amount=TICKET_GATE_PRICE,
        reference="cash-{}".format(admin),
    )

    return {
        "message": f"{len(tickets)} ticket(s) issued and emailed.",
        "ticket_codes": [ticket.ticket_code for ticket in tickets]
    }

@router.post("/tickets/scan")
def scan_ticket( body: dict , req: Request , db: Session = Depends(get_db) ):

    session_id = req.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID not found in cookies")

    ticket_code = body.get('ticket')

    ticket = db.query(Ticket).filter_by(ticket_code=ticket_code).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found. NO ENTRY!")

    if ticket.is_used:
        raise HTTPException(status_code=400, detail="Ticket is already used")
    else:
        ticket.is_used = True
        db.commit()
        db.refresh(ticket)
        return { "message": "Ticket successfully scanned. WELCOME!" }




@router.post("/tickets/resend")
def resend_tickets(body: dict, db: Session = Depends(get_db)):
    email = body.get('email')
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.tickets:
        raise HTTPException(status_code=404, detail="User has no tickets")

    deliver_ticket(user.tickets, user.email)

    return { "message": f"{len(user.tickets)} ticket(s) resent to {email}" }
