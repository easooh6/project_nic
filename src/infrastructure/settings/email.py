from pydantic_settings import BaseSettings

class EmailSettings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_TLS: bool = True

    class Config:
        env_file = ".env"

email_settings = EmailSettings()
