import uuid
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db import get_session_factory, Base
from app.main import app


engine = create_async_engine("sqlite+aiosqlite:///:memory:")
SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def override_get_session_factory():
    database = SessionLocal
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield database
    finally:
        await database().close()


app.dependency_overrides[get_session_factory] = override_get_session_factory


class TestWallet:

    @pytest.mark.asyncio
    async def test_get_wallet(self, client, default_wallet):
        wallet = default_wallet
        response = await client.get(f"/api/v1/wallets/{wallet.wallet_uuid}/")
        assert response.status_code == 200
        assert response.json() == {"amount": 1000}

    @pytest.mark.asyncio
    async def test_get_wallet_with_incorrect_uuid(self, client):
        response = await client.get(f"/api/v1/wallets/{uuid.uuid4()}/")
        assert response.status_code == 404
        assert response.json() == {"detail": "Wallet doesn't exist"}

    @pytest.mark.asyncio
    async def test_deposit(self, client, default_wallet):
        data = {"operationType": "DEPOSIT", "amount": 1000}
        wallet = default_wallet
        response = await client.post(
            f"/api/v1/wallets/{wallet.wallet_uuid}/operation", json=data
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "The deposit was successful, your amount: 2000"
        }

    @pytest.mark.asyncio
    async def test_deposit_with_incorrect_uuid(self, client):
        data = {"operationType": "DEPOSIT", "amount": 1000}
        response = await client.post(
            f"/api/v1/wallets/{uuid.uuid4()}/operation", json=data
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Wallet doesn't exist"}

    @pytest.mark.asyncio
    async def test_withdraw_with_correct_amount(self, client, default_wallet):
        data = {"operationType": "WITHDRAW", "amount": 500}
        wallet = default_wallet
        response = await client.post(
            f"/api/v1/wallets/{wallet.wallet_uuid}/operation", json=data
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "The withdrawal was successful, your amount: 500"
        }

    @pytest.mark.asyncio
    async def test_withdraw_with_incorrect_amount(self, client, default_wallet):
        data = {"operationType": "WITHDRAW", "amount": 5000}
        wallet = default_wallet
        response = await client.post(
            f"/api/v1/wallets/{wallet.wallet_uuid}/operation", json=data
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Insufficient funds on balance"}

    @pytest.mark.asyncio
    async def test_withdraw_with_incorrect_uuid(self, client):
        data = {"operationType": "WITHDRAW", "amount": 500}
        response = await client.post(
            f"/api/v1/wallets/{uuid.uuid4()}/operation", json=data
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Wallet doesn't exist"}
