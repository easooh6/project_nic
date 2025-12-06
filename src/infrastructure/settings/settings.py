from src.infrastructure.settings.db import DBSettings
from src.infrastructure.settings.auth import AuthSettings
from src.infrastructure.settings.redis import RedisSettings
from src.infrastructure.settings.email import EmailSettings
from src.infrastructure.settings.upload import UploadSettings

class Settings:
    def __init__(self):
        self.db = DBSettings()
        self.auth = AuthSettings()
        self.redis = RedisSettings()
        self.email = EmailSettings()
        self.upload = UploadSettings()

settings = Settings()