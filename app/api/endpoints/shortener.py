from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shortener import OriginalUrl, ShortKey, ShortKeyCreate
from app.db.database import get_async_session
from app.repositories.shortener_repository import ShortUrlRepository
from app.services.shortener import generate_short_key

links_router = APIRouter(prefix="/s-link", tags=["ShortUrl"])


async def get_shortener_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ShortUrlRepository:
    return ShortUrlRepository(session)


@links_router.post(
    "/", response_model=ShortKey, status_code=status.HTTP_201_CREATED
)
async def create_short_url(
    url_in: OriginalUrl,
    repo: ShortUrlRepository = Depends(get_shortener_repository),
):
    result = await repo.create_short_url(
        OriginalUrl(
            original_url=url_in.original_url
        ))
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Short-key creating error!",
        )
    return ShortKey(short_key=result.short_key)


@links_router.get(
    "/{shorten_url_id}",
    response_model=OriginalUrl,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def get_original_url(shorten_url_id: str):
    pass
