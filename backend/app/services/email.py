import os
import smtplib
from email.message import EmailMessage
from io import BytesIO


def send_ticket_email(recipient_email: str, pdf_bytes_list: list[bytes | BytesIO]):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    message = EmailMessage()
    message["Subject"] = "Your Experience Afro Ticket 🎟️"
    message["From"] = smtp_user
    message["To"] = recipient_email

    message.set_content(
        "Hi there,\n\nThanks for joining us!\n\nAttached is your ticket.\n\nSee you at the party!\n\nExperience Afro"
    )

    # Loop through each PDF and add it as an attachment
    for i, pdf_bytes in enumerate(pdf_bytes_list):
        # If pdf_bytes is a BytesIO object, we need to read it
        if isinstance(pdf_bytes, BytesIO):
            pdf_bytes = pdf_bytes.read()

        filename = f"ticket_{i + 1}.pdf"  # Give each ticket a unique name
        message.add_attachment(
            pdf_bytes,
            maintype="application",
            subtype="pdf",
            filename=filename
        )

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)

    return f"Ticket sent to {recipient_email}"
