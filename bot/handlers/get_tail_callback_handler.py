from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode

from bot.states.user import MainWindow

router = Router()


@router.callback_query(F.data == 'get_tail')
async def get_tail_callback_handler(callback: CallbackQuery, dialog_manager: DialogManager):
    print("GET_TAIL:", dialog_manager.dialog_data)

    chat_history = dialog_manager.dialog_data.get('chat_history')
    tale_season = dialog_manager.dialog_data.get('tale_season', 1)
    tale_chapter = dialog_manager.dialog_data.get('tale_chapter', 1)
    tale_episode = dialog_manager.dialog_data.get('tale_episode', 1)

    await dialog_manager.start(MainWindow.channel_subscription, mode=StartMode.RESET_STACK,
                               data={"chat_history": chat_history, "tale_season": tale_season,
                                     "tale_chapter": tale_chapter, "tale_episode": tale_episode})

    dialog_manager.dialog_data.update({"chat_history": chat_history, "tale_season": tale_season,
                                     "tale_chapter": tale_chapter, "tale_episode": tale_episode})
