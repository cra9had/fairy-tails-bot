from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import DialogManager

from bot.states.user import MainWindow


router = Router()


@router.callback_query(F.data == 'get_tail')
async def get_tail_callback_handler(message: Message, dialog_manager: DialogManager):
    await message.answer('WORKING!')
