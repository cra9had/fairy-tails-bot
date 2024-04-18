import os
import json

from aiogram.types import ContentType

from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Column, Group, Next, Row, SwitchTo
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.window import Window

from bot.states.user import MainWindow

from bot.getters.user import get_setted_child_settings

from bot.handlers.child_name_handler import child_name_handler

from bot.getters.user import TO_START_BTN, TO_CHILD_SETTINGS_BTN

from bot.on_clicks.user import (
    check_user_setted,
    set_child_gender,
    set_child_age,
    set_child_activities,
)

from bot.texts import GENDER_TEXT, AGE_TEXT, ACTIVITIES_TEXT, NAME_TEXT, CHILD_SETTINGS_TEXT


def get_gender_window():
    window = Window(
        Const(GENDER_TEXT),
        Row(
            Next(Const("👦Мальчик"), id="boy", on_click=set_child_gender),
            Next(Const("👧Девочка"), id="girl", on_click=set_child_gender),
        ),

        state=MainWindow.gender,
    )

    return window


def get_age_window():
    window = Window(
        Const(AGE_TEXT),
        Group(
            *[
                Next(Const(str(i)), id=str(i), on_click=set_child_age)
                for i in range(3, 9)
            ],
            width=2
        ),
        state=MainWindow.age,
    )

    return window


def get_child_activities_window():
    # load all child activities from .env file
    activities = json.loads((os.getenv("ACTIVITIES")))

    window = Window(
        Const(ACTIVITIES_TEXT),
        # parse all activities.
        # idx - a number of the button (starts from 0)
        *[
            Next(Const(i), id=str(idx), on_click=set_child_activities)
            for idx, i in enumerate(activities)
        ],
        state=MainWindow.activities
    )

    return window


def get_name_window():
    window = Window(
        Const(NAME_TEXT),
        MessageInput(child_name_handler, content_types=[ContentType.TEXT]),
        state=MainWindow.name,
    )

    return window


def get_child_settings_window():
    window = Window(
        Format(CHILD_SETTINGS_TEXT),
        Button(Const('Да все верно!'), id='correct'),
        SwitchTo(Const('Изменить данные'), id='to_gender', state=MainWindow.gender),
        getter=get_setted_child_settings,
        state=MainWindow.all_child_settings,
    )

    return window

