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
    short_key = await generate_short_key(repo)
    if short_key is not None:
        return await repo.create_short_url(
            ShortKeyCreate(
                original_url=url_in.original_url, short_key=short_key
            )
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Short-key creating error!",
    )


@links_router.get("/{shorten_url_id}")
async def get_original_url(shorten_url_id: str):
    pass
