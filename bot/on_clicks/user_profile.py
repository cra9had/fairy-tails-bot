from typing import Optional

from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode

from bot.states.user import Profile, Tail



# ----------------------SWITCHERS----------------------


async def switch_to_choosen_tail(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    data = dialog_manager.dialog_data
    await dialog_manager.start(Tail.episode, data=data, mode=StartMode.RESET_STACK)
    

# ----------------------SETTERS----------------------


async def set_previous_page(
        callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data['current_tail_index'] == 1:
        await callback.answer('Вы достигли первой сказки', show_alert=True)
        return
    
    dialog_manager.dialog_data['current_tail_index'] -= 1


async def set_next_page(
        callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data['current_tail_index'] == dialog_manager.dialog_data['max_pages']:
        await callback.answer('Вы достигли последней сказки', show_alert=True)
        return
    
    dialog_manager.dialog_data['current_tail_index'] += 1


async def set_next_episode(
    callback: Optional[CallbackQuery], button: Optional[Button], dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data['current_episode_index'] == 10:
        await dialog_manager.switch_to(Tail.season_ended)
        return
    dialog_manager.dialog_data['current_episode_index'] += 1