from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shortener import OriginalUrl, ShortKey, ShortKeyCreate
from app.db.database import get_async_session
from app.repositories.shortener_repository import ShortUrlRepository

links_router = APIRouter(prefix="/s-link", tags=["ShortUrl"])


async def get_shortener_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ShortUrlRepository:
    return ShortUrlRepository(session)


@links_router.post("/")
async def create_short_url(url_in: OriginalUrl):
    pass


@links_router.get("/{shorten_url_id}")
async def get_original_url(shorten_url_id: str):
    pass
