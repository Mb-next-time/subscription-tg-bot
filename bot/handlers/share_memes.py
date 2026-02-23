import asyncio
from pathlib import Path
import uuid

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, PhotoSize, Document, Video

from bot.keyboards.constants import ButtonText
from bot.keyboards.main_menu import main_menu

max_uploading_media_files_in_one_time = 5

reply_keyboard_markup_share_meme = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="😎Да"),
            KeyboardButton(text="😤Передумал"),
        ]
    ],
    resize_keyboard=True,
)
uploading_file_ready = "👌Все"
uploading_file_finish_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=uploading_file_ready)]],
    resize_keyboard=True,
)
UPLOAD_DIR = "uploads"

router = Router()

class ShareMemes(StatesGroup):
    do_you_want_share_meme = State()
    uploading_file = State()



@router.message(lambda message: message.text == ButtonText.SHARE_MEMES.value)
async def do_you_want_share_meme(message: Message, state: FSMContext) -> None:
    await state.set_state(ShareMemes.do_you_want_share_meme)
    await message.answer(
        "Ты хочешь поделиться своими мемами со мной ?",
        reply_markup=reply_keyboard_markup_share_meme,
    )


@router.message(ShareMemes.do_you_want_share_meme, F.text.casefold() == "😎да")
async def uploading_file_yes(message: Message, state: FSMContext) -> None:
    await state.set_state(ShareMemes.uploading_file)
    await message.answer(
        "🤗Прикрепи медиа файлы (изображения, видео, также можно прикрепить медия, как документ)",
        reply_markup=uploading_file_finish_keyboard,
    )

@router.message(ShareMemes.do_you_want_share_meme, F.text.casefold() == "😤передумал")
async def uploading_file_no(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "🙂Ну нет и нет, пока !",
        reply_markup=main_menu(),
    )

@router.message(ShareMemes.do_you_want_share_meme)
async def do_you_want_share_meme_unknown_choice(message: Message) -> None:
    await message.reply(
        "🤷‍♂️Не понимаю. Выбери \"Да\" или \"Нет\"",
        reply_markup=reply_keyboard_markup_share_meme
    )

async def good_bye(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "😉Пока",
        reply_markup=main_menu(),
    )

@router.message(ShareMemes.uploading_file, F.text.casefold() == uploading_file_ready.lower())
async def uploading_file_ready(message: Message, state: FSMContext) -> None:
    await good_bye(message, state)


def download_attributes_for_video(user_dir, message: Message) -> tuple[str, str]:
    video: Video = message.video
    ext = video.mime_type.split("/")[-1]
    file_path: str = str(user_dir) + f"/{uuid.uuid4()}.{ext}"
    file_id: str = video.file_id

    return file_id, file_path

def download_attributes_for_photo(user_dir, message: Message) -> tuple[str, str]:
    photo: PhotoSize = message.photo[-1]
    file_path: str = str(user_dir) + f"/{uuid.uuid4()}.jpg"
    file_id: str = photo.file_id

    return file_id, file_path

def download_attributes_for_document(user_dir, message: Message) -> tuple[str, str]:
    document: Document = message.document
    ext = document.file_name.split(".")[-1]
    file_path: str = str(user_dir) + f"/{uuid.uuid4()}.{ext}"
    file_id: str = document.file_id

    return file_id, file_path

# 5 MB and 10 MB
photo_max_size = 1024 * 1024 * 5
document_max_size = 1024 * 1024 * 5
video_max_size = 1024 * 1024 * 10

@router.message(
    ShareMemes.uploading_file,
    (F.photo.file_ize > photo_max_size) |
    (F.document.file_size > document_max_size)  |
    (F.video.file_size > video_max_size)
)
async def uploading_file_too_big(message: Message):
    await message.answer(
        text="🫠Медиа файл слишком большой (Видосы не больше 10МБ, картинки не больше 5МБ)",
        reply_markup=uploading_file_finish_keyboard,
    )

@router.message(ShareMemes.uploading_file, F.photo | F.document | F.video)
async def uploading_file(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    count_media_files: int = data.get("count_media_files", 0)

    if count_media_files < max_uploading_media_files_in_one_time:
        user_dir: Path = Path(UPLOAD_DIR + f"/{message.from_user.id}")
        user_dir.mkdir(parents=True, exist_ok=True)
        if message.photo:
            file_id, file_path = download_attributes_for_photo(user_dir, message)
        elif message.document:
            file_id, file_path = download_attributes_for_document(user_dir, message)
        elif message.video:
            file_id, file_path = download_attributes_for_video(user_dir, message)

        text = f"🧐Медиа файлов прикреплено: {count_media_files + 1} из {max_uploading_media_files_in_one_time}"
        await state.update_data({"count_media_files": count_media_files+1})
        await message.bot.download(file_id, destination=file_path)
    else:
        text = "🙄Больше нельзя прикрепить медиа файлы"

    await message.answer(
        text=text,
        reply_markup=uploading_file_finish_keyboard,
    )
