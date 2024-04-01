from typing import Optional

from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode

from states.user import Profile, Tail



# ----------------------SWITCHERS----------------------
async def switch_to_my_tails(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(Profile.my_tails)


async def switch_to_my_subscriptions(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(Profile.my_subscriptions)


async def switch_to_buy_subsription(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    # we reset stack here because we have an access to this window from many other places
    await dialog_manager.start(Profile.subscription, mode=StartMode.RESET_STACK)


async def switch_to_choosen_tail(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    data = dialog_manager.dialog_data
    await dialog_manager.start(Tail.episode,data=data, mode=StartMode.RESET_STACK)


# ----------------------SETTERS----------------------


async def set_previous_page(
        callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data['current_page'] == 1:
        await callback.answer('Вы достигли первой сказки', show_alert=True)
        return
    
    dialog_manager.dialog_data['current_page'] -= 1


async def set_next_page(
        callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data['current_page'] == dialog_manager.dialog_data['max_pages']:
        await callback.answer('Вы достигли последней сказки', show_alert=True)
        return
    
    dialog_manager.dialog_data['current_page'] += 1