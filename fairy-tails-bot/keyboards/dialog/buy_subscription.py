from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const

from states.user import Tail, Profile

from getters.user import TO_START_BTN, TO_BUY_SUB_BTN


def get_buy_subscription():
    window = Window(
        Const('Выберите пакет'),
        Group(
            Button(Const('Аудио формат'), id='audio'),
            Button(Const('Текстовый формат'), id='text'),

            Button(Const("X сказок - 200р"), id='x_audio_tails'),
            Button(Const("X сказок - 100р"), id='x_text_tails'),

            Button(Const("M сказок"), id='m_audio_tails'),
            Button(Const("M сказок"), id='m_text_tails'),

            Button(Const("N сказок"), id='n_audio_tails'),
            Button(Const("N сказок"), id='n_text_tails'),
            
            width=2
        ),

        TO_START_BTN,
        state=Profile.subscription
    )

    return window


def get_user_dont_have_subsription():
    window = Window(
        Const('У вас не приобретён пакет'),
        TO_BUY_SUB_BTN,
        state=Tail.user_dont_have_subscription,
    )

    return window