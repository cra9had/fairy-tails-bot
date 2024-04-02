from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row

from aiogram_dialog.window import Window

from states.user import Tail

from on_clicks.user import buy_new_tail

from getters.user import get_generated_plan_and_photo

def get_tail_window():
    window = Window(
        Format('План сказки на {season} сезон:\n1 эпиздод\n{episodes_1_to_5}\n2 эпизод\n{episodes_5_to_10}'),
        Button(Const('Получить сказку'), id='get_tail', on_click=buy_new_tail),
        state=Tail.tail,
        getter=get_generated_plan_and_photo
    )
    return window