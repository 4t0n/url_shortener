from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ShortUrl
from app.api.schemas.shortener import OriginalUrl, ShortKey
from app.services.shortener import generate_short_key


class ShortUrlRepository:
    model = ShortUrl

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_short_url(
        self, shortener: OriginalUrl, max_attempts: int = 10
    ) -> ShortKey | None:
        for _ in range(max_attempts):
            short_url = ShortUrl(
                original_url=str(shortener.original_url),
                short_key=generate_short_key(),
            )
            self.session.add(short_url)
            try:
                await self.session.commit()
                await self.session.refresh(short_url)
                return ShortKey(short_key=short_url.short_key)
            except IntegrityError:
                await self.session.rollback()
        return None

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
