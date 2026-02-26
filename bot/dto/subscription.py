import datetime
from dataclasses import dataclass

@dataclass
class SubscriptionPeriod:
    interval: str
    step: int

@dataclass
class UserSubscription:
    user_id: int
    subscription_id: int
    expiration_date: datetime.date
    status: str

@dataclass
class Subscription:
    id: int
    description: str
    plan: str
    title: str
    unit_price: int
    currency_code: str
    period: SubscriptionPeriod