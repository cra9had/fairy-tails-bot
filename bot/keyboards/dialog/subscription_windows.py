import operator
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Next, Column, Url, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.getters.user import get_plans
from bot.on_clicks.user import set_selected_plan
from bot.states.user import Subscription

from bot.texts.window_texts import DISCOUNT_TEXT


def get_discount_text_window():
    window = Window(
        Const(DISCOUNT_TEXT),
        Next(Const('Тарифы по Акции')),
        state=Subscription.discount
    )

    return window


def get_subscription_plans_window():

    window = Window(
        Const('Выберите пакет'),

        # Column(
        #     Next(Const("X сказок - 200р"), id='x_tails'),
        #     Next(Const("M сказок"), id='m_tails'),
        #     Next(Const("N сказок"), id='n_tails'),
        # ),
        Column(
            Select(
                Format('{item[0]} - {item[1]}р'),
                id='select_plan',
                item_id_getter=operator.itemgetter(1),
                items='plans',
                on_click=set_selected_plan,
            )
        ),
        getter=get_plans,
        state=Subscription.plans
    )

    return window


def get_buy_subscription_window():
    window = Window(
        Format('К оплате <b>{dialog_data[plan_selected]}р</b>'),
        Column(
            Url(Const("Перейти к оплате"), Const('https://qiwi.com/')),
            Button(Const("Я оплатил"), id='m_tails'),
        ),
        parse_mode='HTML',
        state=Subscription.subscription
    )

    return window
