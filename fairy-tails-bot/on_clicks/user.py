from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode

from states.user import Tail


async def set_tail_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=Tail.all_child_settings, mode=StartMode.RESET_STACK)


async def check_user_setted(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if not dialog_manager.dialog_data['send_data']:
        await callback.answer('Вы должны заполнить все поля', show_alert=True)
        return
    
    # await dialog_manager.switch_to()

async def switch_to_all_children_settings(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Tail.all_child_settings)


async def switch_to_gender(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Tail.gender)


async def set_child_gender(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    # HERE SOME LOGIC TO SET USERS ACTUAL GENDER TO DATABASE
    dialog_manager.dialog_data['gender'] = button.text.text