import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from bot.config import BotSettings
from bot.handlers import start, tariffs, meme




async def main():
    bot_settings = BotSettings()
    bot = Bot(token=bot_settings.TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(meme.router)
    dp.include_router(tariffs.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())