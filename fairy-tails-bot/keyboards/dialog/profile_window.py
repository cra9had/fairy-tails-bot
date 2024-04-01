from aiogram import html

from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row

from aiogram_dialog.window import Window

from states.user import Profile

from getters.user import get_fullname

from on_clicks.start import set_start_dialog
from on_clicks.user_profile import (
    switch_back_to_profile,
    switch_to_buy_subsription,
    switch_to_my_subscriptions,
    switch_to_my_tails
)

def get_profile_window():
    window = Window(
        Format(
            "Кабинет пользователя {full_name}" # get safe full_name text from getter
        ),  
        Button(
            Const("Мои сказки"), 
            id="my_tails", 
            on_click=switch_to_my_tails
        ),
        Button(
            Const("Мои пакеты"), 
            id="my_subscriptions", 
            on_click=switch_to_my_subscriptions
        ),
        Button(
            Const("Приобрести пакет"),
            id="buy_subscription",
            on_click=switch_to_buy_subsription,
        ),

        Button(
            Const("Назад"), 
            id="back_to_start", 
            on_click=set_start_dialog
        ),
        
        state=Profile.my_profile,
        getter=get_fullname,
    )

    return window


def get_my_tails_window():
    window = Window(
        
    )

    return window