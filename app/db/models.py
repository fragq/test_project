from uuid import UUID
from sqlalchemy.orm import Mapped
from .base_model import Base


class Wallet(Base):
    __tablename__ = "wallets"

    wallet_uuid: Mapped[UUID]
    amount: Mapped[int]
