# app/services/ticket_issuer.py

from sqlalchemy.orm import Session
from backend.app.models import User, Ticket, Payment
from backend.app.services.ticket_delivery import deliver_ticket
import uuid

def issue_tickets(
    db: Session,
    email: str,
    quantity: int,
    name: str = None,
    phone: str = None,
    payment_amount: int = 0,
    reference: str = None,
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name, phone=phone)
        db.add(user)
        db.commit()
        db.refresh(user)

    payment = Payment(amount=payment_amount, reference=reference)
    db.add(payment)
    db.commit()
    db.refresh(payment)

    issued_tickets = []
    for _ in range(quantity):
        ticket_code = str(uuid.uuid4())[:8]
        ticket = Ticket(
            ticket_code=ticket_code,
            user_id=user.id,
            payment_id=payment.id
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        issued_tickets.append(ticket)

    deliver_ticket(issued_tickets, user.email)

    return issued_tickets
