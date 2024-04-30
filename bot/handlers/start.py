from datetime import datetime, timezone, timedelta

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler_di import ContextSchedulerDecorator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_dialog import DialogManager, StartMode

from bot.db.orm import get_user_loop
from bot.scheduler.loops import Loop1

from bot.db.models import User, LoopEnum
from bot.states.user import MainWindow
from bot.scheduler.tasks import loop1_task, base_add_job

router = Router()


@router.message(Command('start'))
async def start_cmd(message: Message, dialog_manager: DialogManager, sched: ContextSchedulerDecorator, session: AsyncSession):
    """This handler starts the first task in apscheduler, this task will execute the second one, second will execute
    the third, so when it executes the final third time - this job just will not create next one and the job will
    be deleted from db because this task have 'date' trigger, so it triggers only one time"""

    # WHEN USER USE THE BOT THE FIRST TIME - REGISTER HIM TO DB IN THIS PLACE, otherwise loop_from_db will
    # catch an error (so... user just have to be already registered in db at this moment)

    user_id = message.from_user.id

    loop_from_db: LoopEnum = await get_user_loop(session, user_id)

    # if user clicks on this button first time -> create task
    if loop_from_db is LoopEnum.first:
        next_run = datetime.now(timezone.utc) + timedelta(hours=Loop1.task_1.hour)

        base_add_job(
            sched,
            loop1_task,
            next_run,
            user_id,
            Loop1.task_1,
        )

    # anyway
    await dialog_manager.start(MainWindow.gender, mode=StartMode.RESET_STACK)
