from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.db.models import Wallet
from app.exceptions import WalletNotFoundError
from app.schemas import WalletDTO
from app.uow import UnitOfWorkDep


class WalletService:

    def __init__(self, uow: UnitOfWorkDep):
        self.uow = uow

    async def get_wallet_by_uuid(self, uuid: UUID) -> WalletDTO:
        async with self.uow:
            wallet = await self.uow.walletRepo.get_wallet(wallet_uuid=uuid)
            self._check_existing_of_wallet(wallet)
            return WalletDTO.model_validate(wallet)

    async def deposit_wallet_by_uuid(self, uuid: UUID, amount: int) -> WalletDTO:
        async with self.uow:
            wallet = await self.uow.walletRepo.get_wallet_for_update(wallet_uuid=uuid)
            self._check_existing_of_wallet(wallet)
            wallet.amount += amount
            wallet_to_return = WalletDTO.model_validate(wallet)
            await self.uow.commit()
        return wallet_to_return

    async def withdraw_wallet_by_uuid(self, uuid: UUID, amount: int) -> WalletDTO:
        async with self.uow:
            wallet = await self.uow.walletRepo.get_wallet_for_update(wallet_uuid=uuid)
            self._check_existing_of_wallet(wallet)
            if wallet.amount >= amount:
                wallet.amount -= amount
                wallet_to_return = WalletDTO.model_validate(wallet)
                await self.uow.commit()
                return wallet_to_return

    @staticmethod
    def _check_existing_of_wallet(wallet: Wallet | None):
        if not wallet:
            raise WalletNotFoundError


WalletServiceDep = Annotated[WalletService, Depends(WalletService)]
