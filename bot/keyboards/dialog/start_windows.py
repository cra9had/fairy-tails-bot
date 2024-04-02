from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Back

from aiogram_dialog.window import Window

from bot.states.user import MainWindow, Tail

from bot.getters.user import get_fullname, TO_PROFILE_BTN
from bot.on_clicks.user import to_child

def get_main_window():
    window = Window(
        Format("Привет {full_name}"), # get safe bold full_name from getter
        Row(
            SwitchTo(Const('Подробнее'), state=MainWindow.more_info, id='more_info'),
            TO_PROFILE_BTN
        ),
        Button(Const('Получить сказку(бесплатно)'), id="back_to_start", on_click=to_child),
        state=MainWindow.start,
        getter=get_fullname
    )

    return window


def get_more_info_window():
    window = Window(
        Const('Дополнительная информация'),
        Back(Const('Назад')),
        state=MainWindow.more_info
    )

    return window
