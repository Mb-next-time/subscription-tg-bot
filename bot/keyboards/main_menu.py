from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.keyboards.constants import ButtonText, CallbackFunction

def main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text=ButtonText.GIVE_MEME.value)
    builder.button(text=ButtonText.TARIFFS.value)
    builder.button(text=ButtonText.SHARE_MEMES.value)

    # Forming buttons in rows
    # first line is 2 buttons, seconds line is one button
    builder.adjust(2, 1)

    return builder.as_markup(
        resize_keyboard=True,
    )

def show_surprise_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="\U0001F9D0 А нет Сюрпрайза", callback_data=CallbackFunction.SHOW_TARIFFS.value)

    return builder.as_markup()
