from enum import Enum

from aiogram.filters.callback_data import CallbackData

DAILY_MAX_WITHOUT_SUB = 10
TIME_FOR_DAILY_RESET = 60 * 60 * 24 # 1 day
MEMES_DIR = "media/memes"

class ChooseSubscriptionCallback(CallbackData, prefix="plan"):
    plan: str

class PaySubscriptionCallback(CallbackData, prefix="pay"):
    plan: str

class SubscriptionsCallbackData(Enum):
    SHOW_SUBSCRIPTIONS = "show_subscriptions"
