from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в MemeBot 😎\n\n"
        "7 дней бесплатно, потом подписка.",
        reply_markup=main_menu()
    )