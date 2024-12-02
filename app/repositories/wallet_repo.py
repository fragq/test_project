from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Wallet

from .base_repo import GenericRepository, GenericSQLAlchemyRepository


class BaseWalletRepository(GenericRepository[Wallet], ABC):

    @abstractmethod
    async def get_wallet(self, **filters) -> Wallet: ...

    @abstractmethod
    async def update_wallet(self, data: dict[str, Any], **filters) -> Wallet: ...


class WalletRepository(GenericSQLAlchemyRepository[Wallet], BaseWalletRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Wallet)

    async def get_wallet(self, **filters) -> Wallet:
        wallet = await self.get(**filters)
        return wallet

    async def update_wallet(self, data: dict[str, Any], **filters) -> Wallet:
        wallet = await self.update(data, **filters)
        return wallet
