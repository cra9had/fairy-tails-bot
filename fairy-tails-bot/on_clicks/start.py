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
    data = {}  # LOAD USER TAILS HERE FROM DATABASE!
    await dialog_manager.start(
        state=Profile.my_profile,
        mode=StartMode.RESET_STACK,
    )
    dialog_manager.dialog_data.update(data) # LOAD ALL USER TAILS TO SHOW ONES IN THE FUTURE


async def set_start_dialog(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    # here we should not load any user settings here because there are not any user data in this window
    await dialog_manager.start(
        state=Profile.my_profile,
        mode=StartMode.RESET_STACK,
    )
