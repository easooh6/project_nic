import aiosmtplib
from email.message import EmailMessage
from src.infrastructure.settings.settings import settings

class Email:
    def __init__(self):
        self.host = settings.email.SMTP_HOST
        self.port = settings.email.SMTP_PORT
        self.username = settings.email.SMTP_USER
        self.password = settings.email.SMTP_PASSWORD
        self.email_from = settings.email.EMAIL_FROM
        self.use_tls = settings.email.EMAIL_TLS

    async def send_email(self, to: str, subject: str, body: str):
        message = EmailMessage()
        message["From"] = self.email_from
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            start_tls=self.use_tls,
        )

        return True