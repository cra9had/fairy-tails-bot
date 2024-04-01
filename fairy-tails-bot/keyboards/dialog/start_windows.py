from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row

from aiogram_dialog.window import Window

from states.user import MainWindow

from on_clicks.start import set_tail_dialog, set_profile_dialog

from getters.user import get_fullname

def get_main_window():
    window = Window(
        Format("Привет {full_name}"), # get safe bold full_name from getter
        Row(
            Button(Const("Подробнее"), id="more_info"),
            Button(Const("Мой кабинет"), id="profile", on_click=set_profile_dialog),
        ),
        Button(
            Const("Получить сказку(бесплатно)"), id="get_tail", on_click=set_tail_dialog
        ),
        state=MainWindow.start,
        getter=get_fullname
    )

    return window
