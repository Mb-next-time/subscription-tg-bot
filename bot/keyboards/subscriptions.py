from aiogram.utils.keyboard import InlineKeyboardBuilder


def subscriptions_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="1 месяц — 5₽", callback_data="buy_1")
    builder.button(text="3 месяца — 10₽", callback_data="buy_2")

    # one button in line
    builder.adjust(1)

    return builder.as_markup()