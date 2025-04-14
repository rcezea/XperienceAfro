from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.ticket_issuer import issue_tickets
import os
import hmac
import hashlib


router = APIRouter()
PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET_KEY")
TICKET_PRICE = 5000  # Naira


@router.post("/payments/webhook")
async def paystack_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_paystack_signature: str = Header(None)
):
    raw_body = await request.body()
    computed_signature = hmac.new(
        PAYSTACK_SECRET.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha512,
    ).hexdigest()

    if computed_signature != x_paystack_signature:
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    event = payload.get("event")

    if event != "charge.success":
        return {"status": "ignored"}

    data = payload["data"]
    email = data["customer"]["email"]
    amount_paid_kobo = data["amount"]
    amount_paid_naira = amount_paid_kobo // 100

    num_tickets = amount_paid_naira // TICKET_PRICE
    if num_tickets < 1:
        raise HTTPException(status_code=400, detail="Payment too small for a ticket")

    # Issue the tickets using the reusable service function
    reference = data["reference"]

    issued_tickets = issue_tickets(
        db=db,
        email=email,
        quantity=num_tickets,
        payment_amount=amount_paid_naira,
        reference=reference,
    )

    return {
        "status": "success",
        "tickets_issued": num_tickets,
        "ticket_codes": [ticket.ticket_code for ticket in issued_tickets]
    }

