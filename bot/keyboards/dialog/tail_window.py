from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row

from aiogram_dialog.window import Window

from bot.on_clicks.tale_listing import get_chapter
from bot.states.user import Tail

from bot.on_clicks.user import buy_new_tail, go_chapter

from bot.getters.user import get_generated_plan_and_photo


def get_descr_tail_window():
    window = Window(
        Format('План сказки на {season} сезон:\n {tale_plan}'),
        Button(Const('Получить сказку'), id='get_chapter', on_click=go_chapter),
        state=Tail.tail,
        getter=get_generated_plan_and_photo
    )
    return window


def get_chapter_window():
    window = Window(
        Format('{tale_title}: {season} сезон, {episode} эпизод:\n {chapter_text}'),
        Button(Const('Следующая серия'), id='get_next_chapter', on_click=go_chapter),
        state=Tail.curr_chapter,
        getter=get_chapter
    )
    return window
