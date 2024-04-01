import os
import json

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Column, Row
from aiogram_dialog.widgets.text import Const

from states.user import Tail, Profile

from on_clicks.start import set_start_dialog

from on_clicks.user_profile import switch_to_buy_subsription

from dotenv import load_dotenv

load_dotenv()

AUDIO_SUBS = [i for i in json.loads(os.getenv('AUDIO_SUBS'))]
TEXT_SUBS = json.loads(os.getenv('TEXT_SUBS'))


def get_buy_subscription():
    window = Window(
        Const('Выберите пакет(ДОДЕЛАТЬ ПОРЯДОК ВЫВОДА!)'),
        Row(
            Column(
                Button(Const('Аудио формат'), id='audio'),
                *[Button(Const(i), id=str(idx)) for idx, i in enumerate(AUDIO_SUBS)]
            )
        ),
        Row(
            Column(
                Button(Const('Текстовый формат'), id='text'),
                *[Button(Const(i), id=str(idx)) for idx, i in enumerate(TEXT_SUBS)]
            ),
        ),
        Button(Const('В меню'), id='go_to_start', on_click=set_start_dialog),
        state=Profile.subscription
    )

    return window


def get_user_dont_have_subsription():
    window = Window(
        Const('У вас не приобретён пакет'),
        Button(Const('Приобести'), id='buy_subscription', on_click=switch_to_buy_subsription),
        state=Tail.user_dont_have_subscription,
    )

    return window