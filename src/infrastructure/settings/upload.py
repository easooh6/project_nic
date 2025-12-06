from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import DirectoryPath

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class UploadSettings(BaseSettings):
    DIR: DirectoryPath

    @property
    def UPLOAD_ROOT(self) -> Path:
        return (BASE_DIR / self.DIR).resolve()

    class Config:
        env_file = '.env'
        extra = 'ignore'