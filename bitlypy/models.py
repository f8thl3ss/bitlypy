from uuid import UUID

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.properties import ForeignKey

from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)


class ShortUrl(Base):
    __tablename__ = "short_urls"

    short_url: Mapped[str] = mapped_column(String, primary_key=True)
    original_url: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )


class ApiKey(Base):
    __tablename__ = "api_keys"

    key: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
