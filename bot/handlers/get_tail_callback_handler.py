from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode

from bot.states.user import MainWindow


router = Router()


@router.callback_query(F.data == 'get_tail')
async def get_tail_callback_handler(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(MainWindow.channel_subscription, mode=StartMode.RESET_STACK)
