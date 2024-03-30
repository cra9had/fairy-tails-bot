from aiogram_dialog import DialogManager


async def get_setted_child_settings(dialog_manager: DialogManager, **kwargs):
    gender = f'{dialog_manager.dialog_data.get('gender', False)}'
    name = f'Имя({dialog_manager.dialog_data.get('name', 'Имя')})'
    age = f'Возраст({dialog_manager.dialog_data.get('age', 'Возраст')})'
    activities = f'Увлечения({dialog_manager.dialog_data.get('activites', 'Увлечения')})'
    return {
        'gender': '' if not gender else gender,
        'name': name,
        'age': age,
        'activities': activities,
    }