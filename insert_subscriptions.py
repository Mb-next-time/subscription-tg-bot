import asyncio

from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError

from database import config, models


async def main():
    subs = [
        {
            "plan": "plan_1",
            "title": "План 1 - 100₽",
            "description": "<i><b>План 1</b></i>\n\n"
                           "Доступ к повышенному лимиту мемов до 20 штук в день, на 1 месяц\n\n"
                           "<b>Стоимость - 100₽</b>",
            "unit_price": 10000,
            "period": {
                "interval": "monthly",
                "step": 1,
            },
            "currency_code": "RUB",
        },
        {
            "plan": "plan_2",
            "title": "План 2 - 200₽",
            "description": "<i><b>План 2</b></i>\n\n"
                           "Доступ к повышенному лимиту мемов до 20 штук в день, на 3 месяца\n\n"
                           "<b>Стоимость - 200₽</b>",
            "unit_price": 20000,
            "period": {
                "interval": "monthly",
                "step": 3,
            },
            "currency_code": "RUB",
        },
    ]
    async with config.get_database_session() as session:
        for sub in subs:
            try:
                await session.execute(insert(models.Subscription).values(**sub))
                await session.commit()
            except IntegrityError:
                await session.rollback()

asyncio.run(main())
