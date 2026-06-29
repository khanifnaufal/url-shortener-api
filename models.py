from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from database import Base


class URL(Base):
    """Model database untuk menyimpan data URL yang di-shorten."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    long_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    click_count = Column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<URL id={self.id} short_code='{self.short_code}' long_url='{self.long_url}'>"
