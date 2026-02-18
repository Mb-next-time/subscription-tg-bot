from enum import Enum


class ButtonText(Enum):
    GIVE_MEME = "😂 Получить мем"
    TARIFFS= "💳 Тарифы"

class CallbackFunction(Enum):
    SHOW_TARIFFS = "show_tariffs"
    SHOW_MEMES_NEXT = "show_memes_next"
    SHOW_MEMES_BACK = "show_memes_back"
