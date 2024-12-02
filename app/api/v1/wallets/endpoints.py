from uuid import UUID

from fastapi import APIRouter

from app.schemas import Message, OperationDTO, OperationTypes, WalletDTO
from app.services import WalletServiceDep

router = APIRouter(prefix="/wallets")


@router.post("/{wallet_uuid}/operation")
async def change_amount(
    wallet_uuid: UUID, operation: OperationDTO, service: WalletServiceDep
):
    if operation.operationType == OperationTypes.DEPOSIT:
        wallet = await service.deposit_wallet_by_uuid(wallet_uuid, operation.amount)
        return Message(
            message=f"The deposit was successful, your amount: {wallet.amount}"
        )
    if operation.operationType == OperationTypes.WITHDRAW:
        wallet = await service.withdraw_wallet_by_uuid(wallet_uuid, operation.amount)
        if wallet:
            return Message(
                message=f"The withdrawal was successful, your amount: {wallet.amount}"
                )
        return Message(
            message="Insufficient funds on balance"
        )
        
@router.get("/{wallet_uuid}/", response_model=WalletDTO)
async def get_wallet(wallet_uuid: UUID, service: WalletServiceDep):
    wallet = await service.get_wallet_by_uuid(wallet_uuid)
    return wallet
