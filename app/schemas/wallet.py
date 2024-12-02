from enum import Enum

from pydantic import Field

from .base import BaseDTO


class OperationTypes(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class WalletDTO(BaseDTO):
    amount: int

class OperationDTO(BaseDTO):
    operationType: OperationTypes
    amount: int = Field(ge=0)

class Message(BaseDTO):
    message: str