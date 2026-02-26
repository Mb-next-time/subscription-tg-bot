from sqlalchemy import select, insert, update

from bot import dto
from bot.exceptions import SubscriptionNotFound
from database.config import get_database_session
from database.models import Subscription, User, UserSubscription
from bot.handlers.constants import DAILY_MAX_MEMES_WITH_SUB

cache_in_memory_subscriptions = {}

async def get_subscriptions() -> dict[str, dto.Subscription]:
    if cache_in_memory_subscriptions:
        return cache_in_memory_subscriptions

    async with get_database_session() as database_session:
        subscriptions: list[Subscription] = (await database_session.execute(select(Subscription))).scalars()
        for subscription in subscriptions:
            cache_in_memory_subscriptions[subscription.plan] = dto.Subscription(
                id=subscription.id,
                description=subscription.description,
                currency_code=subscription.currency_code,
                unit_price=subscription.unit_price,
                title=subscription.title,
                plan=subscription.plan,
                period=dto.SubscriptionPeriod(**subscription.period),
            )
    return cache_in_memory_subscriptions

async def get_subscription(plan: str) -> dto.Subscription | None:
    subscription = cache_in_memory_subscriptions.get(plan)
    if subscription:
        return subscription

    async with get_database_session() as database_session:
        subscription: Subscription | None = (
            await database_session.execute(select(Subscription).where(Subscription.plan==plan))
        ).scalar_one_or_none()
    if subscription is None:
        raise SubscriptionNotFound(plan)
    return subscription

async def create_user_subscription(user_subscription: dto.UserSubscription) -> None:
    async with get_database_session() as database_session:
        await database_session.execute(
            insert(UserSubscription)
            .values(
                user_id=user_subscription.user_id,
                subscription_id=user_subscription.subscription_id,
                expiration_date=user_subscription.expiration_date,
                status=user_subscription.status,
            ))
        await database_session.execute(
            update(User)
            .where(User.id == user_subscription.user_id)
            .values(daily_count_max_memes=DAILY_MAX_MEMES_WITH_SUB)
        )
