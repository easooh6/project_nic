from src.infrastructure.settings.db import DBSettings

class Settings:
    def __init__(self):
        self.db = DBSettings()

settings = Settings()