from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.keyboards.constants import ButtonText

min_estimation = 1
max_estimation = 10

reply_keyboard_markup_share_meme = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="😎Да"),
            KeyboardButton(text="😤Нет"),
        ]
    ],
    resize_keyboard=True,
)

router = Router()

class AnonymousSurvey(StatesGroup):
    do_you_like = State()
    estimation = State()
    do_you_want_share_meme = State()
    uploading_file = State()
    final = State()

@router.message(lambda message: message.text == ButtonText.ANONIM_SURVEY.value)
async def init_anonymous_survey(message: Message, state: FSMContext) -> None:
    await state.set_state(AnonymousSurvey.do_you_like)
    await message.answer(
        "Опиши, что нравится в боте",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AnonymousSurvey.do_you_like)
async def estimation(message: Message, state: FSMContext) -> None:
    await state.update_data(do_you_like=message.text)
    await state.set_state(AnonymousSurvey.estimation)
    await message.answer(
        f"Укажи оценку от {min_estimation} до {max_estimation} включительно",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(AnonymousSurvey.estimation)
async def estimation(message: Message, state: FSMContext) -> None:
    retry_message = f"Укажи оценку цифрой от {min_estimation} до {max_estimation} включительно."
    if not message.text.isdigit():
        await message.answer(retry_message)
        return

    user_estimation: int = int(message.text)
    if user_estimation > max_estimation or user_estimation < min_estimation:
        await message.answer(retry_message)
        return

    await state.update_data(estimation=message.text)
    await state.set_state(AnonymousSurvey.do_you_want_share_meme)
    await message.answer(
        f"Ты хочешь поделиться со мной своими мемами ?\n",
        reply_markup=reply_keyboard_markup_share_meme,
    )

@router.message(AnonymousSurvey.do_you_want_share_meme, F.text.casefold() == "😎да")
async def uploading_file_yes(message: Message, state: FSMContext) -> None:
    await state.set_state(AnonymousSurvey.uploading_file)
    await message.answer(
        "🤗Прикрепи изображение",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Передумал")]],
            resize_keyboard=True,
        ),
    )

@router.message(AnonymousSurvey.do_you_want_share_meme, F.text.casefold() == "😤нет")
async def uploading_file_no(message: Message, state: FSMContext) -> None:
    await state.set_state(AnonymousSurvey.final)
    await message.answer(
        "🙂Ну нет и нет, пока !",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AnonymousSurvey.do_you_want_share_meme)
async def do_you_want_share_meme_unknown_choice(message: Message) -> None:
    await message.reply(
        "🤷‍♂️Не понимаю. Выбери \"Да\" или \"Нет\"",
        reply_markup=reply_keyboard_markup_share_meme
    )
