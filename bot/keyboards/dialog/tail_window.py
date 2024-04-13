from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row

from aiogram_dialog.window import Window

from bot.states.user import Tail

from bot.on_clicks.user import buy_new_tail

from bot.getters.user import get_generated_plan_and_photo


def get_tail_window():
    window = Window(
        Format('План сказки на {season} сезон:\n {tale_plan}'),
        Button(Const('Получить сказку'), id='get_tail', on_click=buy_new_tail),
        state=Tail.tail,
        getter=get_generated_plan_and_photo
    )
    return window
