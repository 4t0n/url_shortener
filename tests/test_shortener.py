import pytest

from httpx import ASGITransport, AsyncClient

from fastapi import status

from main import app
from app.api.schemas.shortener import OriginalUrl


@pytest.mark.asyncio
async def test_create_short_url():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://tests/"
    ) as ac:
        payload = {"original_url": "http://127.0.0.1:8080/"}
        response = await ac.post("/s-link/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "short_key" in data
    assert isinstance(data["short_key"], str)


@pytest.mark.asyncio
async def test_get_original_url_redirect():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://tests/"
    ) as ac:
        payload = {"original_url": "http://127.0.0.1:8080/"}
        create_response = await ac.post("/s-link/", json=payload)
        short_key = create_response.json()["short_key"]
        redirect_response = await ac.get(f"/s-link/{short_key}/")
    assert redirect_response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert redirect_response.headers["location"] == payload["original_url"]


@pytest.mark.asyncio
async def test_get_original_url_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://tests/"
    ) as ac:
        response = await ac.get("/s-link/nonexistent_key/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_original_url_validator_valid():
    valid_data = {"original_url": "http://127.0.0.1:8080/"}
    obj = OriginalUrl(**valid_data)
    assert str(obj.original_url) == valid_data["original_url"]


@pytest.mark.asyncio
async def test_original_url_validator_invalid():
    invalid_data = {"original_url": "http://notallowed.com"}
    with pytest.raises(ValueError) as excinfo:
        OriginalUrl(**invalid_data)
    assert "Invalid domain" in str(excinfo.value)


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
