from aiogram.types import ContentType

from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Column
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.window import Window

from states.user import MainWindow, Tail, Profile

from getters.user import get_setted_child_settings

from handlers.child_name_handler import child_name_handler

from on_clicks.user import (
    check_user_setted, 
    set_tail_dialog, 
    switch_to_all_children_settings,
    switch_to_gender,
    set_child_gender,
)

def get_main_window():
    window = Window(
        # Format('Привет {dialog_data.event.from_user.username}'),
        Format('Привет {start_data[user]}'),
        Row(
            Button(Const('Подробнее'), id='more_info'),
            Button(Const('Мой кабинет'), id='profile'),
        ),
        Button(Const('Получить сказку(бесплатно)'), id='get_tail', on_click=set_tail_dialog),
        state=MainWindow.start
    )

    return window


def get_child_settings_window():
    window = Window(
        Const('Настройте сказку под ребёнка'),
        Column(
            Button(
                Format('Пол{gender}'), 
                id='gender',
                on_click=switch_to_gender
            ),
            Button(Format('{name}'), id='name'),
            Button(Format('{age}'), id='age'),
            Button(Format('{activities}'), id='activities'),
            Button(
                Format('Отправить данные'), 
                id='send_data', 
                on_click=check_user_setted
            ),
        ),
        getter=get_setted_child_settings,
        state=Tail.all_child_settings,
    )

    return window 



def get_gender_window():
    window = Window(
        Const('Выберите пол'),
        Button(
            Const('Мальчик'),
            id='boy',
            on_click=set_child_gender
        ),
        Button(
            Const('Девочка'),
            id='girl',
            on_click=set_child_gender
        ),
        Button(
            Const('Назад'), 
            id='back_to_all', 
            on_click=switch_to_all_children_settings
        ),
        state=Tail.gender
    )

    return window 


def get_name_window():
    window = Window(
        Const('Введите имя\n(отправьте сообщением в чат)'),
        MessageInput(child_name_handler, content_types=[ContentType.TEXT]),
        state=Tail.name
    )
    
    return window


def get_profile_window():
    window = Window(
        Const('Privet'),
        state=Profile.my_profile
    )
    return window