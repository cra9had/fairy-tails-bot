import operator
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Next, Column, Url, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.getters.user import get_plans, create_schedule_loop4, get_payment_url
from bot.on_clicks.user import set_selected_plan
from bot.states.user import Subscription

from bot.texts.window_texts import DISCOUNT_TEXT


def get_discount_text_window():
    window = Window(
        Const(DISCOUNT_TEXT),
        Next(Const('Тарифы по Акции')),
        state=Subscription.discount,
        getter=create_schedule_loop4
    )

    return window


def get_subscription_plans_window():

    window = Window(
        Const('Выберите пакет'),
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
            Url(Const("Перейти к оплате"), Format('{payment_url}')),
            Button(Const("Я оплатил"), id='m_tails'),
        ),
        parse_mode='HTML',
        getter=get_payment_url,
        state=Subscription.subscription
    )

    return window
