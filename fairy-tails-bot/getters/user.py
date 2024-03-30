from aiogram_dialog import DialogManager


async def get_setted_child_settings(dialog_manager: DialogManager, **kwargs):
    gender = dialog_manager.dialog_data.get('gender')
    name = dialog_manager.dialog_data.get('name')
    age = dialog_manager.dialog_data.get('age')
    activities = dialog_manager.dialog_data.get('activites')
    return {
        'gender': '' if not gender else f'| {gender}',
        'name': '' if not name else f'| {name}',
        'age': '' if not age else f'| {age}',
        'activities': '' if not activities else f'| {activities}',
    }