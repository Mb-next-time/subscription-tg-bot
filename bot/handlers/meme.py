import os
import random

from aiogram import Router
from aiogram.types import FSInputFile, Message, CallbackQuery, InputMediaPhoto

from bot.keyboards.constants import ButtonText, CallbackFunction
from bot.keyboards.memes import meme_keyboard

MEMES_DIR = "media/memes"
memes = os.listdir(MEMES_DIR)
meme_size = len(memes)
current_index = -1

router = Router()


@router.message(lambda message: message.text == ButtonText.GIVE_MEME.value)
async def show_meme(message: Message):
    global current_index
    current_index = (current_index + 1) % meme_size

    await message.answer_photo(
        photo=FSInputFile(f"{MEMES_DIR}/{memes[current_index]}"),
        caption="Вот ваш мем 😂",
        reply_markup=meme_keyboard(),
        has_spoiler=True,
    )

async def change_media(callback: CallbackQuery):
    global current_index
    new_photo = InputMediaPhoto(
        media=FSInputFile(f"{MEMES_DIR}/{memes[current_index]}"),
        caption="Новый мем 😂"
    )

    await callback.message.edit_media(
        media=new_photo,
        reply_markup=meme_keyboard()
    )

@router.callback_query(lambda callback: callback.data == CallbackFunction.SHOW_MEMES_NEXT.value)
async def show_meme_next(callback: CallbackQuery):
    global current_index
    current_index = (current_index + 1) % meme_size
    await change_media(callback)

@router.callback_query(lambda callback: callback.data == CallbackFunction.SHOW_MEMES_BACK.value)
async def show_meme_back(callback: CallbackQuery):
    global current_index
    current_index = (current_index - 1) % meme_size
    if current_index < 0:
        current_index = meme_size
    await change_media(callback)
