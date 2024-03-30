from typing import Optional

from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode

from states.user import Tail


async def set_tail_dialog(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    data = {}  # LOAD USER SETTED SETTING HERE FROM DATABASE!
    await dialog_manager.start(
        state=Tail.all_child_settings,
        mode=StartMode.RESET_STACK,
        data=data,  # LOAD ALL USER SETTED SETTING TO SHOW ONES IN THE FUTURE
    )


async def check_user_setted(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    if not dialog_manager.dialog_data.get("send_data"):
        await callback.answer("Вы должны заполнить все поля", show_alert=True)
        return

    # await dialog_manager.switch_to()


async def switch_to_all_children_settings(
    callback: Optional[CallbackQuery],
    button: Optional[Button],
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(Tail.all_child_settings)


async def switch_to_gender(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.switch_to(Tail.gender)


async def switch_to_name(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.switch_to(Tail.name)


async def switch_to_age(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.switch_to(Tail.age)


async def set_child_gender(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    # HERE SOME LOGIC TO SET CHILD ACTUAL GENDER TO DATABASE
    dialog_manager.dialog_data["gender"] = button.text.text
    await callback.answer("Пол установлен")
    # return user back to menu
    await switch_to_all_children_settings(None, None, dialog_manager=dialog_manager)


async def set_child_age(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    # HERE SOME LOGIC TO SET CHILD ACTUAL AGE TO DATABASE
    dialog_manager.dialog_data["age"] = button.widget_id
    await callback.answer("Возраст установлен")
    # return user back to menu
    await switch_to_all_children_settings(None, None, dialog_manager=dialog_manager)
