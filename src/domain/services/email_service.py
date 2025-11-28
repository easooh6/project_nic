from src.infrastructure.email import Email

class EmailService:

    def __init__(self):
        self.email_service = Email()


    async def send_email(self, to: str, subject: str, body: str):
        return await self.email_service.send_email(to, subject, body) 

    async def verify_code(code: str) -> bool:
        if code == "corect": #заглушка
            return True