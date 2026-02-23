from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy import insert, select

from bot.keyboards.main_menu import main_menu
from database.config import get_database_session
from database.models import User

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    if state:
        await state.clear()
    async with get_database_session() as database_session:
        telegram_id = message.from_user.id
        user_exists = (await database_session.execute(select(User).where(User.telegram_id == telegram_id))).scalar_one_or_none()
        if user_exists is None:
            statement = insert(User).values(telegram_id=telegram_id)
            await database_session.execute(statement)
    await message.answer(
        "Добро пожаловать в MemeBot 😎",
        reply_markup=main_menu()
    )