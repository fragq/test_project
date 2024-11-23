from abc import ABC, abstractmethod
from typing import Annotated
from fastapi import Depends
from app.db import db_helper
from app.repositories import WalletRepository


class UnitOfWorkBase(ABC):
    walletRepo: WalletRepository

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(UnitOfWorkBase):
    def __init__(self):
        self.session_factory = db_helper.session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.walletRepo = WalletRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


UnitOfWorkDep = Annotated[UnitOfWorkBase, Depends(UnitOfWork)]
