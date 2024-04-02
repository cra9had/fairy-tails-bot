from typing import Optional
from aiogram import html
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.on_clicks.user import to_child, to_profile, to_start, to_buy_subscription

from bot.states.user import Tail


TO_PROFILE_BTN = Button(Const('В профиль'), id='back_to_profile', on_click=to_profile)
TO_START_BTN = Button(Const("В меню"), id="back_to_start", on_click=to_start)
TO_CHILD_SETTINGS_BTN = Button(Const('Назад'), id="back_to_start", on_click=to_child)
TO_BUY_SUB_BTN = Button(Const('Приобрести пакет'), id='buy_sub', on_click=to_buy_subscription)

async def get_full_info_for_dialog(*args, **kwargs):
    dialog_manager: DialogManager = args[1]
    tails = {
            1: {
                'name': 'Сказка о рыбаке и рыбке',
                'season': 2,
            }, 
            2: {
                'name': 'О царевиче и сером волке',
                'season': 1,
            },
            3: {
                'name': 'Иванушка-дурачок',
                'season': 3,
            },
    } # Load all tails from db

    max_pages = 3 # LOAD FROM DATABASE quantity of all the tails for pagination

    user_child_settings = {}  # LOAD USER SETTED SETTING HERE FROM DATABASE!

    current_tail_index = dialog_manager.dialog_data.get('current_tail_index', 1) # if not changed yet

    current_episode_index = dialog_manager.dialog_data.get('current_episode_index', 1) # if not changed yet

    # LOAD USER TAILS HERE FROM DATABASE!
    data = {
        'max_pages': max_pages, 
        'tails': tails,
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
        'gender': '' if not gender else f'| {gender}',
        'name': '' if not name else f'| {name}',
        'age': '' if not age else f'| {age}',
        'activities': '' if not activities else f'| {activities}',
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

    season = dialog_manager.dialog_data['tails'][current_tail_index]['season'] # ('SELECT season FROM tails WHERE tail_index == ?', (current_tail_index, ))

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
        event_from_user: CallbackQuery, dialog_manager: DialogManager, **kwargs
):
    if dialog_manager.dialog_data['from_child_settings']:
        season = 1
    else:
        current_tail_index = dialog_manager.dialog_data['current_tail_index']
        season = dialog_manager.dialog_data['tails'][current_tail_index]['season'] + 1
        

    if season > 1:
        previous_seasons = 'Тексты предыдущих сезонов...' # FROM DATABASE
        promt = f'Сделай мне сказку на основе материала {previous_seasons}' # GENERATE NEW PROMT
    else:
        promt = f'Сделай мне сказку сезон {season}'

    all_episodes_plan = ['сказка'] * 10 # generated text from promt

    episodes_1_to_5 = '\n'.join(all_episodes_plan[:6])
    episodes_5_to_10 = '\n'.join(all_episodes_plan[6:])
    return {
        'season': season,
        'episodes_1_to_5': episodes_1_to_5,
        'episodes_5_to_10': episodes_5_to_10,
    }