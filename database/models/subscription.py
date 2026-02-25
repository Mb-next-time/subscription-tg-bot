from datetime import datetime, timezone

from sqlalchemy import String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.config import Base

class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(256))
    plan: Mapped[str] = mapped_column(String(16), unique=True)
    title: Mapped[str] = mapped_column(String(32))
    unit_price: Mapped[int] = mapped_column(default=0)
    period: Mapped[str] = mapped_column(JSON)
    currency_code: Mapped[str] = mapped_column(String(3))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
