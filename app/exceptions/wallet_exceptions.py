from fastapi import HTTPException, status


class BaseCustomHTTPExeception(HTTPException): ...


WalletNotFoundError = BaseCustomHTTPExeception(
    status_code=status.HTTP_404_NOT_FOUND, detail="Wallet doesn't exist"
)
