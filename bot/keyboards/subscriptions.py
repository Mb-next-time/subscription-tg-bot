from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Subscription
from bot.handlers.constants import SubscriptionsCallbackData
from bot import dto


def subscriptions_keyboard(subscriptions: dict[str, dto.Subscription]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for plan in subscriptions:
        builder.button(text=subscriptions[plan].title, callback_data=f"plan:{plan}")
    # one button per line
    builder.adjust(1)

    return builder.as_markup()

def subscription_keyboard(subscription: dto.Subscription = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Оплатить", callback_data="pay:" + subscription.plan)
    builder.button(text="Назад", callback_data=SubscriptionsCallbackData.SHOW_SUBSCRIPTIONS.value)
    # two button per line
    builder.adjust(2)

    return builder.as_markup()