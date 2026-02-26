from datetime import datetime, timezone, timedelta

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.config import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    daily_count: Mapped[int] = mapped_column(default=0)
    daily_count_max_memes: Mapped[int] = mapped_column(default=10)
    timestamp_first_count: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc) - timedelta(days=1))
