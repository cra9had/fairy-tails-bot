from aiogram.types import ContentType

from magic_filter import F

from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.window import Window

from states.user import Profile, Tail

from getters.user import get_fullname

from on_clicks.start import set_start_dialog, set_profile_dialog

from on_clicks.user_profile import (
    switch_to_buy_subsription,
    switch_to_my_subscriptions,
    switch_to_my_tails,
    switch_to_choosen_tail,
    set_previous_page,
    set_next_page,
)

from getters.user import (
    get_my_tails,
    get_current_tail,

)

BACK_TO_PROFILE = Button(Const('Назад'), id='back_to_profile',on_click=set_profile_dialog)

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
        Format('Сказка {current_tail}'),
        Row(
            Button(Const('<'), id='previous_page', on_click=set_previous_page),
            Button(Format('{current_page}/{max_pages}'), id='pagination'),
            Button(Const('>'), id='next_page', on_click=set_next_page),
        ),
        Button(Const('Выбрать'), id='choose_tail', on_click=switch_to_choosen_tail),
        BACK_TO_PROFILE,
        state=Profile.my_tails,
        getter=get_my_tails
    )

    return window


def get_current_tail_window():
    window = Window(
        Format('Сказка номер {current_tail_index}\nНазвание серии {current_episode_text}'),
        StaticMedia(url=Format('{photo}'), type=ContentType.PHOTO),
        Button(Const('Получить аудио файл к сказке', when=F['dialog_data']['can_have_audio']), id='get_audio'),
        Button(Const('Следующая серия'), id='next_episode'),
        BACK_TO_PROFILE,
        getter=get_current_tail,
        state=Tail.episode
    )

    return window