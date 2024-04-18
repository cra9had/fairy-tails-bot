from pprint import pprint
from typing import Optional
from aiogram import html
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from sqlalchemy.ext.asyncio import AsyncSession

from bot.on_clicks.user import to_child, to_profile, to_start, to_buy_subscription
from bot.services.gpt import ChatGPT
from bot.services.tales_prompts import TaleGenerator

TO_PROFILE_BTN = Button(Const('В профиль'), id='back_to_profile', on_click=to_profile)
TO_START_BTN = Button(Const("В меню"), id="back_to_start", on_click=to_start)
TO_CHILD_SETTINGS_BTN = Button(Const('Назад'), id="back_to_start", on_click=to_child)
TO_BUY_SUB_BTN = Button(Const('Приобрести пакет'), id='buy_sub', on_click=to_buy_subscription)


async def get_full_info_for_dialog(*args, **kwargs):
    dialog_manager: DialogManager = args[1]
    user_child_settings = {}  # LOAD USER SETTED SETTING HERE FROM DATABASE!

    current_tail_index = dialog_manager.dialog_data.get('current_tail_index', 1)

    current_episode_index = dialog_manager.dialog_data.get('current_episode_index', 1)

    # LOAD USER TAILS HERE FROM DATABASE!
    data = {
        'user_child_settings': user_child_settings,
        'current_tail_index': current_tail_index,
        'current_episode_index': current_episode_index,

    }

    # upload all collected settings to dialog
    dialog_manager.dialog_data.update(data)


async def get_setted_child_settings(dialog_manager: DialogManager, **kwargs):
    gender = dialog_manager.dialog_data.get('gender')
    name = dialog_manager.dialog_data.get('name')
    age = dialog_manager.dialog_data.get('age')
    activities = dialog_manager.dialog_data.get('activities')
    return {
        'gender': gender,
        'name': name,
        'age': age,
        'activities': activities,
    }


async def get_fullname(
        event_from_user: Message, dialog_manager: DialogManager, **kwargs
):
    safe_bold_full_name = html.bold(html.quote(event_from_user.full_name))
    return {
        'full_name': safe_bold_full_name
    }


async def get_my_tails(
        dialog_manager: DialogManager, **kwargs
):
    current_tail_index: int = dialog_manager.dialog_data.get('current_tail_index', 1)
    max_pages: int = dialog_manager.dialog_data['max_pages']
    current_tail: str = dialog_manager.dialog_data['tails'].get(current_tail_index)

    data = {
        'current_tail_index': current_tail_index,
        'max_pages': max_pages,
        'current_tail': current_tail
    }

    return data


async def get_current_tail(
        event_from_user: CallbackQuery, dialog_manager: DialogManager, **kwargs
):
    # number of the choosen tail from pagination
    current_tail_index = dialog_manager.start_data['current_tail_index']

    # GET something about episode: text, name, maybe short description FROM DATABASE
    current_episode_index: int = dialog_manager.dialog_data['current_episode_index']
    current_episode_text = dialog_manager.dialog_data['tails'][current_tail_index]['name']

    season = dialog_manager.dialog_data['tails'][current_tail_index][
        'season']  # ('SELECT season FROM tails WHERE tail_index == ?', (current_tail_index, ))

    # GET file_id for current episode or link or smth else FROM DATABASE
    photo_for_episode = 'https://i0.wp.com/mynintendonews.com/wp-content/uploads/2019/09/fairy_tail.jpg?resize=930%2C620&ssl=1'

    return {
        'season': season,
        'photo': photo_for_episode,
        'current_tail_index': current_tail_index,
        'current_episode_index': current_episode_index,
        'current_episode_text': current_episode_text,
    }


async def get_generated_plan_and_photo(
        event_from_user: CallbackQuery, dialog_manager: DialogManager, session: AsyncSession, **kwargs
):
    if dialog_manager.dialog_data['from_child_settings']:
        season = 1
        episode = 1
        tale_generator = TaleGenerator()

    else:
        current_tail_index = dialog_manager.dialog_data['current_tail_index']
        season = dialog_manager.dialog_data['tails'][current_tail_index]['season'] + 1
        tale_generator = dialog_manager.dialog_data['tale_generator'] or TaleGenerator()

    tale_plan = await tale_generator.generate_tale_plan(name=dialog_manager.dialog_data.get("name"),
                                                        sex=dialog_manager.dialog_data.get("gender"),
                                                        age=dialog_manager.dialog_data.get("age"),
                                                        interests=dialog_manager.dialog_data.get("activities")
                                                        )

    tale_title = await tale_generator.generate_tale_title()

    dialog_manager.dialog_data.update({'tale_plan': tale_plan,
                                       'tale_title': tale_title,
                                       'session': session,
                                       'season': season,
                                       'tale_generator': tale_generator})

    return {
        'season': season,
        'tale_plan': tale_plan,
    }
