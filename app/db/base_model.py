from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.core import settings


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.db.NAMING_CONVENTION)
    id: Mapped[int] = mapped_column(primary_key=True)
