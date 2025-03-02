from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ShortUrl
from app.api.schemas.shortener import OriginalUrl, ShortKey, ShortKeyCreate


class ShortUrlRepository:
    model = ShortUrl

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_short_url(self, shortener: ShortKeyCreate) -> ShortKey:
        short_url = ShortUrl(**shortener.model_dump())
        self.session.add(short_url)
        await self.session.commit()
        await self.session.refresh(short_url)
        return ShortKey(short_key=short_url.short_key)

    async def get_url(self, short_key: ShortKey) -> OriginalUrl | None:
        result = await self.session.execute(
            select(ShortUrl).where(ShortUrl.short_key == short_key.short_key)
        )
        row = result.scalar_one_or_none()
        return (
            OriginalUrl.model_validate({"original_url": row.original_url})
            if row
            else None
        )
