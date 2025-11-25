from src.infrastructure.email import EmailService

email_service = EmailService()
async def send_email(to: str, subject: str, body: str):
    return await email_service.send_email(to, subject, body) 

async def verify_code(code: str) -> bool:
    if code == "corect": #заглушка
        return True