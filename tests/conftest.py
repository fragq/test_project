from uuid import uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.db import Base, Wallet
from app.main import app

from .test_api import SessionLocal, engine


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


async def lifespan():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def db():
    try:
        await lifespan()
        yield SessionLocal()
    except Exception as e:
        print(f"An error occurred while setting up the database: {e}")


@pytest_asyncio.fixture(scope="function")
async def default_wallet(db):
    try:
        wallet_data = {
            "wallet_uuid": uuid4(),
            "amount": 1000,
        }
        wallet = Wallet(
            wallet_uuid=wallet_data["wallet_uuid"], amount=wallet_data["amount"]
        )
        db.add(wallet)
        await db.commit()
        await db.refresh(wallet)
        print("Default user added to database")
        yield wallet
    except Exception as e:
        print(f"An error occurred while adding default user: {e}")
        await db.rollback()
