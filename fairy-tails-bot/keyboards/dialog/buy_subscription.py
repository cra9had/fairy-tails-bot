from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const

from states.user import Tail, Profile

from on_clicks.start import set_start_dialog

from on_clicks.user_profile import switch_to_buy_subsription


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