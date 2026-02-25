import logging

from sqlalchemy import select

from bot.exceptions import SubscriptionNotFound
from database.config import get_database_session
from database.models import Subscription

logger = logging.getLogger(__name__)

async def get_subscriptions() -> list[Subscription]:
    async with get_database_session() as database_session:
        subscriptions: list[Subscription] = (await database_session.execute(select(Subscription))).scalars()
    return subscriptions

async def get_subscription(plan: str) -> Subscription:
    subscription = None
    async with get_database_session() as database_session:
        subscription: Subscription | None = (await database_session.execute(select(Subscription).where(Subscription.plan==plan))).scalar_one_or_none()
    if subscription is None:
        logger.exception(f"Subscription {plan!r} not found")
        raise SubscriptionNotFound
    return subscription
