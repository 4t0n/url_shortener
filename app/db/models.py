from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ShortUrl(Base):
    """
    Модель для хранения соответствия оригинальных и коротких URL.
    """
    __tablename__ = "short_url"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(
        String(2083), nullable=False
    )
    short_key: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )
