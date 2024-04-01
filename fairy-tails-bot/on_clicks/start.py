from typing import Optional

from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode

from states.user import Tail, MainWindow, Profile


async def set_tail_dialog(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    data = {}  # LOAD USER SETTED SETTING HERE FROM DATABASE!
    await dialog_manager.start(
        state=Tail.all_child_settings,
        mode=StartMode.RESET_STACK,
    )
    dialog_manager.dialog_data.update(data) # LOAD ALL USER SETTED SETTING TO SHOW ONES IN THE FUTURE


async def set_profile_dialog(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):  
    tails = {
        1: 'Сказка о рыбаке и рыбке', 
        2: 'О царевиче и сером волке', 
        3: 'Иванушка-дурачок',
    }

    max_pages = 3

    season = dialog_manager.dialog_data.get('season', 0) + 1

    can_have_audio: bool = dialog_manager.middleware_data['can_have_audio']

    # LOAD USER TAILS HERE FROM DATABASE!
    data = {
        'season': season,
        'can_have_audio': can_have_audio,
        'current_tail_index': 1, # default starts from first tail DONT CHANGE
        'max_pages': max_pages, # LOAD FROM DATABASE quantity of all the tails for pagination
        'tails': tails
        }  
    
    await dialog_manager.start(
        state=Profile.my_profile,
        mode=StartMode.RESET_STACK,
    )
    dialog_manager.dialog_data.update(data) # LOAD ALL USER TAILS TO SHOW ONES IN THE FUTURE


async def set_start_dialog(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(
        state=MainWindow.start,
        data=dialog_manager.dialog_data,
        mode=StartMode.RESET_STACK,
    )
