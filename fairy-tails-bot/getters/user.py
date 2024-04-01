from aiogram import html
from aiogram.types import Message

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


async def get_fullname(event_from_user: Message, dialog_manager: DialogManager, **kwargs):
    safe_bold_full_name = html.bold(html.quote(event_from_user.full_name))
    return {
        'full_name': safe_bold_full_name
    }