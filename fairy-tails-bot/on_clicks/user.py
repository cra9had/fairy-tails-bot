from typing import Optional

from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode

from states.user import Tail


async def buy_new_tail(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_subscribed: bool = dialog_manager.middleware_data['user_subscribed']

    if not user_subscribed:
        await dialog_manager.switch_to(Tail.user_dont_have_subscription)



async def check_user_setted(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    all_settings = {"gender", "name", "age", "activities"}
    setted: bool = (not dialog_manager.dialog_data.keys() ^ all_settings)

    if setted:
        await dialog_manager.switch_to(Tail.tail)

    elif not dialog_manager.dialog_data.get("can_send_data"):
        await callback.answer("Вы должны заполнить все поля", show_alert=True)
        return


# ----------------------SWITCHERS----------------------


async def switch_to_all_children_settings(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
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


async def switch_to_activities(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.switch_to(Tail.activities)


async def switch_to_getting_tail(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.switch_to(Tail.tail)

# ----------------------SETTERS----------------------


async def set_child_activities(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    # HERE SOME LOGIC TO SET CHILD ACTUAL ACTIVITY TO DATABASE
    dialog_manager.dialog_data["activities"] = button.text.text
    await callback.answer("Увлечения установлены")
    # return user back to menu
    await switch_to_all_children_settings(None, None, dialog_manager=dialog_manager)


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
