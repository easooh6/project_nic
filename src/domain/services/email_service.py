import aiosmtplib
from email.message import EmailMessage
from src.infrastructure.settings.email import email_settings

class EmailService:
    def __init__(self):
        self.host = email_settings.SMTP_HOST
        self.port = email_settings.SMTP_PORT
        self.username = email_settings.SMTP_USER
        self.password = email_settings.SMTP_PASSWORD
        self.email_from = email_settings.EMAIL_FROM
        self.use_tls = email_settings.EMAIL_TLS

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