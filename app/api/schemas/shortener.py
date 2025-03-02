from typing import Annotated
from urllib.parse import urlparse

from pydantic import BaseModel, HttpUrl, StringConstraints, field_validator

from app.core.config import settings


class ShortKey(BaseModel):
    short_key: Annotated[str, StringConstraints(max_length=10)]


class OriginalUrl(BaseModel):
    original_url: HttpUrl

    @field_validator("original_url")
    @classmethod
    def check_domain(cls, value: HttpUrl):
        parsed = urlparse(str(value))
        if parsed.netloc not in settings.ALLOWED_DOMAINS:
            raise ValueError("Invalid domain!")
        return value


class ShortKeyCreate(OriginalUrl, ShortKey):
    pass
