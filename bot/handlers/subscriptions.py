from aiogram import Router
from aiogram.types import CallbackQuery,Message

from bot.keyboards.subscriptions import subscriptions_keyboard
from bot.keyboards.constants import ButtonText, CallbackFunction

MEMES_DIR = "media/memes"

router = Router()


@router.callback_query(lambda c: c.data == CallbackFunction.SHOW_SUBSCRIPTIONS.value)
async def inline_show_tariffs(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите план:",
        reply_markup=subscriptions_keyboard()
    )
    await callback.answer()

@router.message(lambda message: message.text == ButtonText.SUBSCRIPTIONS.value)
async def show_tariffs(message: Message):

    await message.answer(
        "Выберите план:",
        reply_markup=subscriptions_keyboard()
    )

