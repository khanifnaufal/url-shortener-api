from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator


class ShortenRequest(BaseModel):
    """Schema untuk request POST /shorten."""

    long_url: HttpUrl
    custom_alias: Optional[str] = None
    expires_in_hours: Optional[int] = None

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
            if len(v) > 20:
                raise ValueError("custom_alias maksimal 20 karakter")
        return v

    @field_validator("expires_in_hours")
    @classmethod
    def expires_must_be_non_negative(cls, v: Optional[int]) -> Optional[int]:
        """Pastikan expires_in_hours tidak negatif."""
        if v is not None and v < 0:
            raise ValueError("expires_in_hours tidak boleh negatif")
        return v


class ShortenResponse(BaseModel):
    """Schema untuk response POST /shorten."""

    short_code: str
    short_url: str
    long_url: str
    created_at: datetime
    expires_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class URLStatsResponse(BaseModel):
    """Schema untuk response GET /stats/{short_code}."""

    short_code: str
    long_url: str
    click_count: int
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_expired: bool
    qr_url: str

    model_config = {"from_attributes": True}


class URLDetailResponse(BaseModel):
    """Schema detail URL lengkap untuk list semua URL."""

    short_code: str
    short_url: str
    long_url: str
    click_count: int
    created_at: datetime

    model_config = {"from_attributes": True}

