from aiogram import html
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager


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
    current_page: int = dialog_manager.dialog_data.get('current_page')
    max_pages: int = dialog_manager.dialog_data['max_pages']
    current_tail: str = dialog_manager.dialog_data['tails'][current_page] # LOAD HERE ALL USER`S TAILS
    
    data = {
        'current_page': current_page,
        'max_pages': max_pages,
        'current_tail': current_tail
    }
    
    return data


async def get_current_tail(
        event_from_user: CallbackQuery, dialog_manager: DialogManager, **kwargs
):
    dialog_manager.dialog_data.update(dialog_manager.start_data)
    current_tail_index = dialog_manager.dialog_data['current_page']
    
    # GET something about episode: text, name, maybe short description FROM DATABASE
    current_episode_text = dialog_manager.dialog_data.get('current_episode_text')

    # GET file_id for current episode or link or smth else FROM DATABASE
    photo_for_episode = 'https://i0.wp.com/mynintendonews.com/wp-content/uploads/2019/09/fairy_tail.jpg?resize=930%2C620&ssl=1'

    return {
        'photo': photo_for_episode,
        'current_tail_index': current_tail_index,
        'current_episode_text': current_episode_text,
    }
