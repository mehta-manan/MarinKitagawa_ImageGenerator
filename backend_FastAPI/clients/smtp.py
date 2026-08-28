import os

import smtplib
from email.message import EmailMessage

import logging
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()
    
class _SMTPClient:
    def __init__(self):
        self._host = os.getenv('SMTP_HOST')
        self._port = os.getenv('SMTP_PORT')
        self._user = os.getenv('SMTP_USER')
        self._pass = os.getenv('SMTP_PASS')
        self._mail_from = os.getenv('MAIL_FROM')

    def _build_email_message(self, to_address, subject, content, image_attachment):
        msg = EmailMessage()

        msg['Subject'] = subject
        msg['From'] = self._mail_from
        msg['To'] = to_address
        
        # plain-text fallback for email clients that do not support HTML
        msg.set_content(content["text"])
        # HTML content
        msg.add_alternative(content["html"], subtype='html')

        # Attach the image
        image_bytes = image_attachment["image_bytes"]
        image_filename = image_attachment["filename"]
        image_maintype = image_attachment["maintype"]
        image_subtype = image_attachment["subtype"]
        msg.add_attachment(image_bytes, maintype=image_maintype, subtype=image_subtype, filename=image_filename)

        return msg

    def _send_message(self, msg):
        try:
            with smtplib.SMTP_SSL(self._host, self._port) as server:
                server.login(self._user, self._pass)
                server.send_message(msg)
                logger.info(f"Email sent successfully to: {msg['To']} with subject: {msg['Subject']}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")

    def send_email(self, to_address, subject, content, image_attachment):
        logger.info(f"Preparing to send email to: {to_address} with subject: {subject}")
        msg = self._build_email_message(to_address, subject, content, image_attachment)
        self._send_message(msg)

smtp_client = _SMTPClient()