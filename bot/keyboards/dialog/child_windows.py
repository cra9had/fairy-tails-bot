import os
import json

from aiogram.types import ContentType

from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Column, Group, SwitchTo
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.window import Window

from bot.states.user import Tail

from bot.getters.user import get_setted_child_settings

from bot.handlers.child_name_handler import child_name_handler

from bot.getters.user import TO_START_BTN, TO_CHILD_SETTINGS_BTN

from bot.on_clicks.user import (
    check_user_setted,
    set_child_gender,
    set_child_age,
    set_child_activities,
)


def get_child_settings_window():
    window = Window(
        Const("Настройте сказку под ребёнка"),
        Column(
            SwitchTo(Format("Пол{gender}"), id="gender", state=Tail.gender),
            SwitchTo(Format("Имя{name}"), id="name", state=Tail.name),
            SwitchTo(Format("Возраст{age}"), id="age", state=Tail.age),
            SwitchTo(Format("Увлечения{activities}"), id="activities", state=Tail.activities),
            
            Button(Const("Отправить данные"), id="send_data", on_click=check_user_setted),
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
        TO_CHILD_SETTINGS_BTN,
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
        TO_CHILD_SETTINGS_BTN,
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
        TO_CHILD_SETTINGS_BTN,
        state=Tail.activities
    )

    return window