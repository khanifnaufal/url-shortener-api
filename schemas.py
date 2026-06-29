from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator


class ShortenRequest(BaseModel):
    """Schema untuk request POST /shorten."""

    long_url: HttpUrl
    custom_alias: Optional[str] = None

    @field_validator("custom_alias")
    @classmethod
    def alias_must_be_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
        """Pastikan custom_alias hanya berisi huruf, angka, dan tanda hubung."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
            if not all(c.isalnum() or c == "-" for c in v):
                raise ValueError("custom_alias hanya boleh berisi huruf, angka, dan tanda hubung (-)")
            if len(v) > 50:
                raise ValueError("custom_alias maksimal 50 karakter")
        return v


class ShortenResponse(BaseModel):
    """Schema untuk response POST /shorten."""

    short_code: str
    short_url: str
    long_url: str
    created_at: datetime

    model_config = {"from_attributes": True}
