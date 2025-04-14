from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


def create_ticket_pdf(ticket_code: str, qr_image: BytesIO) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 20)
    c.drawString(100, height - 100, f"Your Party Ticket")
    c.setFont("Helvetica", 14)
    c.drawString(100, height - 130, f"Ticket Code: {ticket_code}")

    # Draw QR code image
    c.drawInlineImage(qr_image, 100, height - 330, width=150, height=150)

    c.save()
    buffer.seek(0)
    return buffer
