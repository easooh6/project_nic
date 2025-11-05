from src.infrastructure.db.models.base import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.db.models.user import User


class FileUpload(Base):
    __tablename__ = "file_upload"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer)
    mime: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    owner_user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)
    owner_user: Mapped["User"] = relationship("User", back_populates="file_upload", uselist=False)

   


# новый формат моделей SQLAlchemy 2.0  #
# https://habr.com/ru/articles/848592/ #