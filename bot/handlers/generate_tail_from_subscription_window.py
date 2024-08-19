from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode


from bot.states.user import MainWindow

router = Router()


@router.callback_query(F.data == 'generate_tail_from_subscription_window')
async def generate_tail_from_subscription_window(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(MainWindow.all_child_settings, mode=StartMode.RESET_STACK)