import os
import json

from aiogram.types import ContentType

from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Column, Group
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.window import Window

from states.user import Tail, Profile

from getters.user import get_setted_child_settings

from handlers.child_name_handler import child_name_handler

from getters.user import TO_START_BTN, TO_CHILD_SETTINGS_BTN

from on_clicks.user import (
    check_user_setted,
    switch_to_all_children_settings,
    switch_to_gender,
    set_child_gender,
    switch_to_name,
    switch_to_age,
    set_child_age,
    switch_to_activities,
    set_child_activities,
)


def get_child_settings_window():
    window = Window(
        Const("Настройте сказку под ребёнка"),
        Column(
            Button(Format("Пол{gender}"), id="gender", on_click=switch_to_gender),
            Button(Format("Имя{name}"), id="name", on_click=switch_to_name),
            Button(Format("Возраст{age}"), id="age", on_click=switch_to_age),
            Button(
                Format("Увлечения{activities}"),
                id="activities",
                on_click=switch_to_activities,
            ),
            Button(
                Const("Отправить данные"), id="send_data", on_click=check_user_setted
            ),
            TO_START_BTN,
        ),
        getter=get_setted_child_settings,
        state=Tail.all_child_settings,
    )

    return window


def get_gender_window():
    window = Window(
        Const("Выберите пол"),
        Button(Const("Мальчик"), id="boy", on_click=set_child_gender),
        Button(Const("Девочка"), id="girl", on_click=set_child_gender),
        TO_CHILD_SETTINGS_BTN,
        state=Tail.gender,
    )

    return window


def get_name_window():
    window = Window(
        Const("Введите имя\n(отправьте сообщением в чат)"),
        MessageInput(child_name_handler, content_types=[ContentType.TEXT]),
        Button(
            Const("Отменить ввод"),
            id="cancel_input",
            on_click=switch_to_all_children_settings,
        ),
        state=Tail.name,
    )

    return window


def get_age_window():
    window = Window(
        Const("Выберите возраст"),
        Group(
            *[
                Button(Const(str(i)), id=str(i), on_click=set_child_age)
                for i in range(3, 9)
            ],
            width=2
        ),
        Button(
            Const("Назад"),
            id="back_to_all",
            on_click=switch_to_all_children_settings,
        ),
        state=Tail.age,
    )

    return window


def get_child_activities_window():
    # load all child activities from .env file
    activities = json.loads((os.getenv("ACTIVITIES")))

    window = Window(
        Const("Выберите интересы вашего ребёнка"),
        # parse all activities.
        # idx - a number of the button (starts from 0)
        *[
            Button(Const(i), id=str(idx), on_click=set_child_activities)
            for idx, i in enumerate(activities)
        ],
        Button(
            Const("Назад"),
            id="back_to_all",
            on_click=switch_to_all_children_settings,
        ),
        state=Tail.activities
    )

    return window