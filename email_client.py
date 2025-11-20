import smtplib
import os
import dotenv
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

dotenv.load_dotenv()

SUBJECT = "CABW Black Electives Database"
SENDER = os.getenv("EMAIL_SENDER")
PASSWORD = os.getenv("EMAIL_PASS")

def send_email(body, recipients, subject=SUBJECT, sender=SENDER, password=PASSWORD, is_html=True):
    """
    Send an email via SMTP

    Args:
        body (str): Email body content (plain text or HTML)
        recipients (list): List of recipient email addresses
        subject (str): Email subject line
        sender (str): Sender email address
        password (str): Sender email password
        is_html (bool): Whether the body is HTML (default: True)
    """
    try:
        # Create message container
        if is_html:
            msg = MIMEMultipart('alternative')
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = ", ".join(recipients)

            # Create HTML and plain text parts
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
        else:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = ", ".join(recipients)

        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print(f"Message sent successfully to {', '.join(recipients)}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
