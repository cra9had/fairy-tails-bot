from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Column
from aiogram_dialog.window import Window

from states.user import MainWindow


def get_main_window():
    window = Window(
        # Format('Привет {dialog_data.event.from_user.username}'),
        Format('Привет {start_data[user]}'),
        Row(
            Button(Const('Подробнее'), id='more_info'),
            Button(Const('Мой кабинет'), id='profile'),
        ),
        Button(Const('Получить сказку(бесплатно)'), id='get_tail'),
        state=MainWindow.my_profile
    )

    return window


def get_child_settings():
    window = Window(
        Column(
            Button(Format('{gender}'), id='gender'),
            Button(Format('{name}'), id='name'),
            Button(Format('{age}'), id='age'),
            Button(Format('{acti}'), id='activites'),
            Button(Format('Отправить данные'), id='send_data'),
        ),
        getter=get_setted_child_settings
    )