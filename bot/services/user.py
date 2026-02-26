from sqlalchemy import select

from bot.exceptions.user import UserNotFound
from database.config import get_database_session
from bot import dto
from database.models import User

async def get_user(telegram_id: int) -> dto.User | None:
    async with get_database_session() as database_session:
        database_user: User = (await database_session.execute(
            select(User).where(User.telegram_id == telegram_id))).scalar_one_or_none()
        if database_user is None:
            raise UserNotFound(telegram_id)
        user = dto.User(
            id=database_user.id,
            telegram_id=database_user.telegram_id,
            daily_count=database_user.daily_count,
            timestamp_first_count=database_user.timestamp_first_count,
        )
        return user
