import asyncio
import pytest

from typing import AsyncGenerator

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import StaticPool

from main import app
from app.db.database import Base, get_async_session
from app.api.schemas.shortener import OriginalUrl
from app.core.config import settings


test_engine = create_async_engine(
    settings.TEST_DATABASE,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = async_sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    async def setup():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(setup())
    yield

    async def teardown():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await test_engine.dispose()
    asyncio.run(teardown())


async def override_get_async_session() -> AsyncGenerator:
    connection = await test_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, expire_on_commit=False)
    await session.begin_nested()
    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()


app.dependency_overrides[get_async_session] = override_get_async_session

client = TestClient(app)


def test_create_short_url():
    payload = {"original_url": "http://127.0.0.1:8080/"}
    response = client.post("/s-link/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "short_key" in data


def test_get_original_url_redirect():
    payload = {"original_url": "http://127.0.0.1:8080/"}
    create_response = client.post("/s-link/", json=payload)
    short_key = create_response.json()["short_key"]
    response = client.get(f"/s-link/{short_key}/", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert "location" in response.headers
    assert response.headers["location"] == "http://127.0.0.1:8080/"


def test_get_original_url_not_found():
    response = client.get("/s-link/nonexistent/")
    assert response.status_code == 404


def test_original_url_validator_valid():
    valid_data = {"original_url": "http://127.0.0.1:8080/"}
    obj = OriginalUrl(**valid_data)
    assert str(obj.original_url) == valid_data["original_url"]


def test_original_url_validator_invalid():
    invalid_data = {"original_url": "http://notallowed.com"}
    with pytest.raises(ValueError) as excinfo:
        OriginalUrl(**invalid_data)
    assert "Invalid domain" in str(excinfo.value)
