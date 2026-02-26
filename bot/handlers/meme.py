from datetime import datetime, timezone
import os

from aiogram import Router
from aiogram.types import FSInputFile, Message
from sqlalchemy import select, update, insert, or_, func

from bot.keyboards.constants import ButtonText
from bot.handlers.constants import DAILY_MAX_WITHOUT_SUB, TIME_FOR_DAILY_RESET, MEMES_DIR
from database.config import get_database_session
from database.models import User, ViewContent, Content


memes = os.listdir(MEMES_DIR)

router = Router()


@router.message(lambda message: message.text == ButtonText.GIVE_MEME.value)
async def show_meme(message: Message) -> None:
    async with get_database_session() as database_session:
        telegram_id = message.from_user.id
        user: User = (await database_session.execute(select(User).where(User.telegram_id == telegram_id).with_for_update())).scalar_one_or_none()
        time_is_passed = (datetime.now(timezone.utc) - user.timestamp_first_count).total_seconds()
        if time_is_passed >= TIME_FOR_DAILY_RESET:
            user.daily_count = 0
        if user.daily_count >= DAILY_MAX_WITHOUT_SUB:
            await message.answer(
                text="Ваш лимит мемов достиг максимума на сегодня 🥲\nВозвращайтесь через сутки 🤤"
            )
            return

        content = (await database_session.execute(select(Content).outerjoin(
            ViewContent, ViewContent.content_id == Content.id
        ).where(
            (ViewContent.id == None) | (ViewContent.user_id != user.id),
            ).order_by(func.random()).limit(1))).scalar_one_or_none()
        if content is None:
            await message.answer(text=f"@{message.from_user.username} контент закончился 👀\nПополним в скором времени 🚀")
            return

        file = FSInputFile(content.path)
        caption = f"Вот ваш мем 😂 (Осталось {DAILY_MAX_WITHOUT_SUB - user.daily_count - 1})"
        update_date: dict[str, datetime | int] = {
            "daily_count": user.daily_count + 1,
        }
        if user.daily_count == 0:
            update_date.update({"timestamp_first_count": datetime.now(timezone.utc)})

        await database_session.execute(
            update(User)
            .where(
                User.telegram_id == telegram_id)
            .values(**update_date))
        await database_session.execute(insert(ViewContent).values(
            user_id=user.id,
            content_id=content.id,
        ))

    if content.type == 'image':
        await message.answer_photo(
            photo=file,
            caption=caption,
        )
    elif content.type == 'video':
        await message.answer_video(
            video=file,
            caption=caption
        )
