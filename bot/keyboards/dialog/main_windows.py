import os
import json

from aiogram.types import ContentType

from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Column, Group, Next, Row, SwitchTo
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.window import Window

from bot.states.user import MainWindow

from bot.db.orm import  save_child_settings_to_db

from bot.getters.user import get_setted_child_settings, create_task_to_tail, create_task_to_episode

from bot.handlers.child_name_handler import child_name_handler

from bot.on_clicks.user import (
    check_user_setted,
    set_child_gender,
    set_child_age,
    set_child_activities, check_user_subscribed,
)

from bot.texts import *


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
        Next(Const('Да все верно!'), id='correct', on_click=save_child_settings_to_db),
        SwitchTo(Const('Изменить данные'), id='to_gender', state=MainWindow.gender),
        getter=get_setted_child_settings,
        state=MainWindow.all_child_settings,
    )

    return window


def get_waiting_tail_window():
    """
    This window does not have any buttons. It uses a getter argument to switch state to MainWindow.wait_tail inside
    create_task_to_tail function. It`s really useful: we don`t create an additional functionality in previous Window.
    In previous window we have save_child_settings_to_db but it`s not a good idea to switch state to
    MainWindow.wait_tail inside this function(it`s just illogical)
    """
    window = Window(
        Const(WAIT_GENERATION_TEXT),
        state=MainWindow.wait_tail,
        getter=create_task_to_tail,  # just a trick to change state to waiting
    )

    return window


def get_channel_subscription_window():
    window = Window(
        Const(CHANNEL_SUB_TEXT),
        Button(Const('Есть подписка'), id='check_sub_btn', on_click=check_user_subscribed),
        state=MainWindow.channel_subscription
    )

    return window


def get_waiting_episode_window():
    """
    This is the same getter trick as in get_waiting_task_window function
    This window does not have any buttons. It uses a getter argument to switch state to MainWindow.wait_episode inside
    create_task_to_episode function. It`s really useful: we don`t create an additional functionality in previous Window.
    In previous window we have check_user_subscribed but it`s not a good idea to switch state to
    MainWindow.wait_episode inside this function(it`s just illogical)
        """
    window = Window(
        Const(TIP_TEXT),
        state=MainWindow.wait_episode,
        getter=create_task_to_episode,
    )

    return window
