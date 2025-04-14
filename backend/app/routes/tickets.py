from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import User
from backend.app.services.ticket_delivery import deliver_ticket
import os

router = APIRouter()
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


@router.post("/tickets/generate")
def generate_ticket_admin(
    request: dict,
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    from backend.app.services.ticket_issuer import issue_tickets

    email = request.get('email')  # Get email from the body
    quantity = request.get('quantity', 1)
    phone = request.get('phone', "0")
    name = request.get('name', "")
    price = request.get('price', 0)

    tickets = issue_tickets(
        db=db,
        email=email,
        quantity=quantity,
        name=name,
        phone=phone,
        payment_amount=price,
        reference="cash",
    )

    return {
        "message": f"{len(tickets)} ticket(s) issued and emailed.",
        "ticket_codes": [ticket.ticket_code for ticket in tickets]
    }

@router.post("/tickets/resend")
def resend_tickets(request: dict, db: Session = Depends(get_db)):
    email = request.get('email')
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.tickets:
        raise HTTPException(status_code=404, detail="User has no tickets")

    for ticket in user.tickets:
        deliver_ticket(ticket, user.email)

    return {"message": f"{len(user.tickets)} ticket(s) resent to {email}"}
