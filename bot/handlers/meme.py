import os
import random

from aiogram import Router
from aiogram.types import FSInputFile, Message

from bot.keyboards.constants import ButtonText

MEMES_DIR = "media/memes"
memes = os.listdir(MEMES_DIR)

router = Router()


@router.message(lambda message: message.text == ButtonText.GIVE_MEME.value)
async def show_meme(message: Message):
    meme_file = random.choice(memes)

    await message.answer_photo(
        photo=FSInputFile(f"{MEMES_DIR}/{meme_file}"),
        caption="Вот ваш мем 😂",
    )
