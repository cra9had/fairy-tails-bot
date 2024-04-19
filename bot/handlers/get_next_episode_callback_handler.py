from aiogram import Router, F
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_dialog import DialogManager, StartMode, ShowMode

from bot.states.user import MainWindow, Subscription

from bot.db.orm import get_user_have_sub

router = Router()


@router.callback_query(F.data == 'get_next_episode')
async def get_next_episode_callback_handler(
        callback: CallbackQuery, dialog_manager: DialogManager, session: AsyncSession=None
):
    user_have_sub = dialog_manager.middleware_data['user_subscribed']
    if user_have_sub:
        await dialog_manager.start(MainWindow.wait_episode, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(Subscription.discount, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)
        await callback.answer()
