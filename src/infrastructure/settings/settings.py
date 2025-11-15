from src.infrastructure.settings.db import DBSettings
from src.infrastructure.settings.auth import AuthSettings
class Settings:
    def __init__(self):
        self.db = DBSettings()
        self.auth = AuthSettings()

settings = Settings()