import asyncio
from aiogram import Bot, Dispatcher

from bot.config import CommonSettings
from bot.handlers import start, tariffs, meme


async def main():
    common_setting = CommonSettings()
    bot = Bot(token=common_setting.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(meme.router)
    dp.include_router(tariffs.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())