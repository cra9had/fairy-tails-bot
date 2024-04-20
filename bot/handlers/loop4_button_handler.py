from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode

from bot.states.user import Subscription


router = Router()


@router.callback_query(F.data == 'discount_button')
async def loop4_button_handler(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(Subscription.plans, mode=StartMode.RESET_STACK)
