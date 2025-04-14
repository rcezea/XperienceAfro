from backend.app.services.qr import generate_qr_code
from backend.app.services.pdf import create_ticket_pdf
from backend.app.services.email import send_ticket_email
from backend.app.models import Ticket


def deliver_ticket(ticket: list[Ticket], email: str):
    pdf_list = []
    for ticket in ticket:
        qr = generate_qr_code(ticket.ticket_code)
        pdf = create_ticket_pdf(ticket.ticket_code, qr)
        pdf_list.append(pdf)
    send_ticket_email(email, pdf_list)
