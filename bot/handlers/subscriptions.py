import enum
import json
import logging
from datetime import datetime, date, timezone

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from dateutil.relativedelta import relativedelta

from bot import dto
from bot.exceptions import SubscriptionNotFound
from bot.handlers.constants import ChooseSubscriptionCallback, SubscriptionsCallbackData, PaySubscriptionCallback
from bot.keyboards.subscriptions import subscriptions_keyboard, subscription_keyboard
from bot.keyboards.constants import ButtonText
from bot.services import get_subscriptions, get_subscription, create_user_subscription
from bot.services.user import get_user
from bot.handlers.constants import SubscriptionLiteral

from main import bot_settings

router = Router()

class PaymentPayload(enum.Enum):
    TELEGRAM_ID = "telegram_id"
    SUBSCRIPTION_PLAN = "subscription_plan"


@router.callback_query(lambda c: c.data == SubscriptionsCallbackData.SHOW_SUBSCRIPTIONS.value)
async def inline_show_subscriptions(callback: CallbackQuery) -> None:
    subscriptions = await get_subscriptions()
    await callback.message.edit_text(
        "Выберите план:",
        reply_markup=subscriptions_keyboard(subscriptions)
    )
    await callback.answer()

@router.message(lambda message: message.text == ButtonText.SUBSCRIPTION.value)
async def show_subscriptions(message: Message):
    subscriptions = await get_subscriptions()
    await message.answer(
        "Выберите план:",
        reply_markup=subscriptions_keyboard(subscriptions)
    )

@router.callback_query(ChooseSubscriptionCallback.filter())
async def inline_show_subscription(
    callback: CallbackQuery,
    callback_data: ChooseSubscriptionCallback
) -> None:
    plan = callback_data.plan
    try:
        subscription = await get_subscription(plan)
        await callback.message.edit_text(
            subscription.description,
            parse_mode="HTML",
            reply_markup=subscription_keyboard(subscription)
        )
    except SubscriptionNotFound:
        await callback.message.edit_text(
            "План не найден ❌",
            reply_markup=callback.message.reply_markup
        )

    await callback.answer()


@router.callback_query(PaySubscriptionCallback.filter())
async def pay_subscription(
    callback: CallbackQuery,
    callback_data: PaySubscriptionCallback,
) -> None:
    # Payment in minimal unit of currency
    # For RUB is 'копейка'
    plan = callback_data.plan
    try:
        subscription = await get_subscription(plan)
        prices = [LabeledPrice(label=subscription.title, amount=subscription.unit_price)]
        telegram_id = callback.from_user.id
        payload = {
            PaymentPayload.TELEGRAM_ID.value: telegram_id,
            PaymentPayload.SUBSCRIPTION_PLAN.value: subscription.plan,
        }
        payload_json = json.dumps(payload)
        await callback.message.answer_invoice(
            title=f"Подписка на {subscription.title}",
            description="Доступ к расширенным лимитам",
            payload=payload_json,
            provider_token=bot_settings.PAYMENT_PROVIDER_TOKEN,
            currency=subscription.currency_code,
            prices=prices,
        )
    except SubscriptionNotFound as exception:
        logging.exception(exception)
        await callback.message.edit_text(
            "План для оплаты не найден ❌",
            reply_markup=callback.message.reply_markup
        )

@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery) -> None:
    logging.info(pre_checkout_query)
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message) -> None:
    payment = message.successful_payment
    logging.info(payment)
    await message.answer("Оплата прошла успешно 🎉")
    payload = json.loads(payment.invoice_payload)
    subscription = await get_subscription(payload[PaymentPayload.SUBSCRIPTION_PLAN.value])
    user = await get_user(payload[PaymentPayload.TELEGRAM_ID.value])
    expiration_date = None
    if subscription.period.interval == SubscriptionLiteral.Period.MONTHLY.value:
        expiration_date = datetime.now(timezone.utc) + relativedelta(months=subscription.period.step)

    user_subscription = dto.UserSubscription(
        user_id=user.id,
        subscription_id=subscription.id,
        expiration_date=expiration_date,
        status=SubscriptionLiteral.Status.ACTIVE.value,
    )
    await create_user_subscription(user_subscription)
