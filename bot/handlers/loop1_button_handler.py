from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode

from bot.states.user import MainWindow


router = Router()


@router.callback_query(F.data == 'start_button')
async def loop1_button_handler(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(MainWindow.gender, mode=StartMode.RESET_STACK)