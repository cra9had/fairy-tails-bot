from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

from bot.states.user import MainWindow
from bot.scheduler.tasks import test_task

from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()


@router.message(Command('start'))
async def start_cmd(message: Message, dialog_manager: DialogManager, sched: AsyncIOScheduler,):
    user_id = message.from_user.id

    sched.add_job(
        test_task,
        'interval',
        seconds=2,
        id=str(user_id),
        kwargs={'user_id': user_id}
    )
    await dialog_manager.start(MainWindow.gender, mode=StartMode.RESET_STACK)
