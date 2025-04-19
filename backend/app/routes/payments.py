import hashlib
import hmac
import os

from backend.app.database import get_db
from backend.app.services.ticket_controller import issue_tickets
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter()
PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET_KEY")
TICKET_PRICE_NAIRA = int(os.getenv("TICKET_PRICE"))
TICKET_PRICE_KOBO = TICKET_PRICE_NAIRA * 100


@router.post("/payments/webhook")
async def paystack_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_paystack_signature: str = Header(None)
):

    # Verify Paystack webhook signature
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
    reference = data["reference"]

    # Ensure the amount is a multiple of ticket price
    if amount_paid_kobo % TICKET_PRICE_KOBO != 0:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid payment amount ({amount_paid_kobo}) not a multiple of ticket price ({TICKET_PRICE_KOBO})"
        )

    num_tickets = amount_paid_kobo // TICKET_PRICE_KOBO
    if num_tickets < 1:
        raise HTTPException(status_code=400, detail="Payment too small for at least one ticket")

    issued_tickets = issue_tickets(
        db=db,
        email=email,
        quantity=num_tickets,
        payment_amount=amount_paid_kobo // 100,
        reference=reference,
    )

    return {
        "status": "success",
        "tickets_issued": num_tickets,
        "ticket_codes": [ticket.ticket_code for ticket in issued_tickets]
    }

