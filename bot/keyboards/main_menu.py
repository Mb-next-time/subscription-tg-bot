from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.keyboards.constants import ButtonText

def main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text=ButtonText.GIVE_MEME.value)
    builder.button(text=ButtonText.SUBSCRIPTION.value)
    builder.button(text=ButtonText.SHARE_MEMES.value)

    # Forming buttons in rows
    # first line is 2 buttons, seconds line is one button
    builder.adjust(2, 1)

    return builder.as_markup(
        resize_keyboard=True,
    )
