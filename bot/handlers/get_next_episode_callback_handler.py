from contextlib import suppress

import aiogram_dialog
from aiogram import Router, F
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_dialog import DialogManager, StartMode, ShowMode

from bot.states.user import MainWindow, Subscription

from bot.db.orm import get_user_have_sub

router = Router()


@router.callback_query(F.data == 'get_next_episode')
async def get_next_episode_callback_handler(
        callback: CallbackQuery, dialog_manager: DialogManager, session: AsyncSession = None
):

    user_have_sub = dialog_manager.middleware_data['user_subscribed']
    if user_have_sub:
        print("GET_NEXT_EPISODE:", dialog_manager.dialog_data)

        chat_history = dialog_manager.dialog_data.get('chat_history')
        tale_season = dialog_manager.dialog_data.get('tale_season')
        tale_chapter = dialog_manager.dialog_data.get('tale_chapter')
        tale_episode = dialog_manager.dialog_data.get('tale_episode')
        print("IN GET NEXT EPISODE HANDLER: SEASON-CHAP-EPISODE:", tale_season, tale_chapter, tale_episode)

        await dialog_manager.start(MainWindow.wait_episode, mode=StartMode.RESET_STACK,
                                   data={"chat_history": chat_history, "tale_season": tale_season,
                                         "tale_chapter": tale_chapter, "tale_episode": tale_episode})

    else:
        await dialog_manager.start(Subscription.discount, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)
        await callback.answer()
