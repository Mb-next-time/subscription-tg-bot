from aiogram.utils.keyboard import InlineKeyboardBuilder


def tariffs_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="1 месяц — 100₽", callback_data="buy_1")
    builder.button(text="3 месяца — 250₽", callback_data="buy_3")
    builder.button(text="⬅ Сюрпрайз", callback_data="show_surprise")

    # one button in line
    builder.adjust(1)

    return builder.as_markup()