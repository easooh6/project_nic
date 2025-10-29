from datetime import datetime
from src.infrastructure.db.models.base import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship, Mapped, mapped_column



class FileUpload(Base):
    __tablename__ = "file_upload"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer)
    mime: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)

    owner_user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)
    owner_user: Mapped["User"] = relationship(back_populates="file_upload")

   


# новый формат моделей SQLAlchemy 2.0  #
# https://habr.com/ru/articles/848592/ #