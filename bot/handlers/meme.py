import os
import random

from aiogram import Router
from aiogram.types import FSInputFile, Message, CallbackQuery, InputMediaPhoto

from bot.keyboards.constants import ButtonText, CallbackFunction
from bot.keyboards.memes import meme_keyboard

MEMES_DIR = "media/memes"
memes = os.listdir(MEMES_DIR)
current_index = -1

router = Router()


@router.message(lambda message: message.text == ButtonText.GIVE_MEME.value)
async def show_meme(message: Message):
    global current_index
    while True:
        new_index = random.randint(1, len(memes) - 1)
        if current_index != new_index:
            current_index = new_index
            break

    await message.answer_photo(
        photo=FSInputFile(f"{MEMES_DIR}/{memes[current_index]}"),
        caption="Вот ваш мем 😂",
        reply_markup=meme_keyboard(),
        has_spoiler=True,
    )

@router.callback_query(lambda callback: callback.data == CallbackFunction.SHOW_MEMES.value)
async def show_meme(callback: CallbackQuery):
    global current_index
    while True:
        new_index = random.randint(1, len(memes) - 1)
        if current_index != new_index:
            current_index = new_index
            break

    new_photo = InputMediaPhoto(
        media=FSInputFile(f"{MEMES_DIR}/{memes[current_index]}"),
        caption="Новый мем 😂"
    )

    await callback.message.edit_media(
        media=new_photo,
        reply_markup=meme_keyboard()
    )
