from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.constants import CallbackFunction

def meme_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(text="Назад 🍌", callback_data=CallbackFunction.SHOW_MEMES_BACK.value)
    builder.button(text="Дальше 💥", callback_data=CallbackFunction.SHOW_MEMES_NEXT.value)

    return builder.as_markup()
