from datetime import datetime, timezone
import os
import random

from aiogram import Router
from aiogram.types import FSInputFile, Message
from sqlalchemy import select, update

from bot.keyboards.constants import ButtonText
from bot.handlers.constants import DAILY_MAX_WITHOUT_SUB, TIME_FOR_DAILY_RESET
from database.config import get_database_session
from database.models import User

MEMES_DIR = "media/memes"
memes = os.listdir(MEMES_DIR)

router = Router()


@router.message(lambda message: message.text == ButtonText.GIVE_MEME.value)
async def show_meme(message: Message):
    async with get_database_session() as database_session:
        meme_file = random.choice(memes)
        telegram_id = message.from_user.id
        user: User = (await database_session.execute(select(User).where(User.telegram_id == telegram_id))).scalar_one_or_none()
        time_is_passed = (datetime.now(timezone.utc) - user.timestamp_first_count).seconds
        if time_is_passed >= TIME_FOR_DAILY_RESET:
            user.daily_count = 0
        if user.daily_count >= DAILY_MAX_WITHOUT_SUB:
            await message.answer(
                text="Ваш лимит мемов достиг максимума на сегодня 🥲\nВозвращайтесь через сутки 🤤"
            )
            return

        await message.answer_photo(
            photo=FSInputFile(f"{MEMES_DIR}/{meme_file}"),
            caption=f"Вот ваш мем 😂 (Осталось {DAILY_MAX_WITHOUT_SUB - user.daily_count - 1})",
        )
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
