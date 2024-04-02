from aiogram.types import ContentType

from magic_filter import F

from aiogram_dialog.widgets.text import Format, Const, Case
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Group, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.window import Window

from bot.states.user import Profile, Tail, MainWindow

from bot.getters.user import get_fullname

from bot.on_clicks.user_profile import (
    switch_to_choosen_tail,
    set_previous_page,
    set_next_page,
    set_next_episode,
)

from bot.getters.user import (
    get_my_tails,
    get_current_tail,
)

from bot.getters.user import TO_PROFILE_BTN, TO_START_BTN, TO_BUY_SUB_BTN

from bot.on_clicks.user import (
    send_audio_file
)

def get_profile_window():
    window = Window(
        Format(
            "Кабинет пользователя {full_name}" # get safe full_name text from getter
        ),  
        SwitchTo(
            Const("Мои сказки"), 
            id="my_tails", 
            state=Profile.my_tails
        ),
        SwitchTo(
            Const("Мои пакеты"), 
            id="my_subscriptions", 
            state=Profile.my_subscriptions
        ),
        TO_BUY_SUB_BTN,
        TO_START_BTN,

        state=Profile.my_profile,
        getter=get_fullname,
    )

    return window


def selector(data, case: Case, manager):
    return bool(manager.dialog_data['tails'])

def get_my_tails_window():
    window = Window(
        Case(
            {
                True: Format('Сказка {current_tail}'),
                False: Const('У вас ещё нет сказок'),
            },
            selector=selector,
        ),
        Group(
            Row(
                Button(Const('<'), id='previous_page', on_click=set_previous_page),
                Button(Format('{current_tail_index}/{max_pages}'), id='pagination'),
                Button(Const('>'), id='next_page', on_click=set_next_page),
            ),
            Button(Const('Выбрать'), id='choose_tail', on_click=switch_to_choosen_tail),
            TO_PROFILE_BTN,
            when=F['dialog_data']['tails'], # at least 1 tail exists,
            id='tails_exist',
        ),
        Group(
            TO_START_BTN,
            id='tails_not_exist',
            when=~F['dialog_data']['tails'],
        ),
        state=Profile.my_tails,
        getter=get_my_tails,
    )

    return window


def get_current_tail_window():
    window = Window(
        Format('Сезон {season}\nСказка номер {current_tail_index}\nНомер серии {current_episode_index}'),
        StaticMedia(url=Format('{photo}'), type=ContentType.PHOTO),
        Button(Const('Получить аудио файл к сказке', when=F['middleware_data']['can_have_audio']), id='get_audio', on_click=send_audio_file),
        Button(Const('Следующая серия'), id='next_episode', on_click=set_next_episode),
        TO_PROFILE_BTN,
        getter=get_current_tail,
        state=Tail.episode
    )

    return window


def get_episode_ended_window():
    window = Window(
        Const('Эпизод окончен, он находится в вашем личном кабинете.'),
        TO_START_BTN,
        SwitchTo(Const('Получить следующий сезон'), id='get_next_season', state=Tail.tail),
        state=Tail.season_ended
    )

    return window


def get_my_subscriptions_window():
    window = Window(
        Const('1) Пакет на N сказок, осталось Z дней'),
        Const('2) Пакет на N сказок, осталось X дней'),
        TO_BUY_SUB_BTN,
        TO_PROFILE_BTN,
        state=Profile.my_subscriptions
    )

    return window