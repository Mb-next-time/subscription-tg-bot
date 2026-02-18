from aiogram import Router
from aiogram.types import CallbackQuery,Message

from bot.keyboards.main_menu import show_surprise_menu
from bot.keyboards.tariffs import tariffs_keyboard
from bot.keyboards.constants import ButtonText, CallbackFunction

MEMES_DIR = "media/memes"

router = Router()


@router.callback_query(lambda c: c.data == CallbackFunction.SHOW_TARIFFS.value)
async def inline_show_tariffs(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите тариф:",
        reply_markup=tariffs_keyboard()
    )
    await callback.answer()

@router.message(lambda message: message.text == ButtonText.TARIFFS.value)
async def show_tariffs(message: Message):

    await message.answer(
        "Выберите тариф:",
        reply_markup=tariffs_keyboard()
    )


@router.callback_query(lambda c: c.data == "show_surprise")
async def show_surprise(callback: CallbackQuery):
    await callback.message.edit_text(
        "Вернуться к тарифам",
        reply_markup=show_surprise_menu()
    )
    await callback.answer()
