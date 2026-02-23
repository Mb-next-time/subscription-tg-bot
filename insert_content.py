import asyncio
from pathlib import Path

from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError

from database import config, models
from bot.handlers.constants import MEMES_DIR


async def main():
    path_memes: Path = Path(MEMES_DIR)
    async with config.get_database_session() as session:
        for entry in path_memes.iterdir():
            _, ext = entry.name.split('.')
            try:
                if ext == 'jpg':
                    content_type = 'image'
                else:
                    content_type = 'video'
                await session.execute(insert(models.Content).values(path=f"{path_memes}/{entry.name}", type=content_type))
                await session.commit()
            except IntegrityError:
                await session.rollback()

asyncio.run(main())
