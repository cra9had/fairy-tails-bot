from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

from states.user import MainWindow


router = Router()


@router.message(Command('start'))
async def start_cmd(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainWindow.start, mode=StartMode.RESET_STACK)