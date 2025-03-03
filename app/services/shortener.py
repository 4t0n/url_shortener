import random
import string

from app.api.schemas.shortener import ShortKey
from app.repositories.shortener_repository import ShortUrlRepository


async def generate_short_key(
    repo: ShortUrlRepository,
    length: int = 6,
    max_attempts: int = 10,
) -> str | None:
    for _ in range(max_attempts):
        key = "".join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )
        result = await repo.get_url(ShortKey(short_key=key))
        if result is None:
            return key
    return None
