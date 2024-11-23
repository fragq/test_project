from fastapi import APIRouter
from .wallets import wallets_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(wallets_router)
