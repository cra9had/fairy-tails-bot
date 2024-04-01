from typing import Optional

from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode

from states.user import Profile



# ----------------------SWITCHERS----------------------

async def switch_back_to_profile(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    await dialog_manager.start(state=Profile.my_profile, data=dialog_manager.dialog_data, mode=StartMode.RESET_STACK)


async def switch_to_my_tails(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(Profile.all_users_tails)


async def switch_to_my_subscriptions(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(Profile.my_subscriptions)


async def switch_to_buy_subsription(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    # we reset stack here because we have an access to this window from many other places
    await dialog_manager.start(Profile.subscription, mode=StartMode.RESET_STACK)