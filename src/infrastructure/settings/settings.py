<<<<<<< HEAD
from src.infrastructure.settings.db import DBSettings

class Settings:
    def __init__(self):
        self.db = DBSettings()

settings = Settings()
=======
from src.infrastructure.settings.db import DBSettings

class Settings:
    def __init__(self):
        self.db = DBSettings()

settings = Settings()
>>>>>>> 2ebb10f (refactor: update async CRUD for AuditLog using get_db_session pattern)
