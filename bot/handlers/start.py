from datetime import datetime, timezone, timedelta

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_dialog import DialogManager, StartMode

from bot.scheduler.loops import Loop1

from bot.db.models import User, LoopEnum
from bot.states.user import MainWindow
from bot.scheduler.tasks import loop1_task

from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()


@router.message(Command('start'))
async def start_cmd(message: Message, dialog_manager: DialogManager, sched: AsyncIOScheduler, session: AsyncSession):
    # REGISTER USER TO DB HERE

    user_id = message.from_user.id

    res = await session.execute(select(User).filter_by(tg_id=user_id))

    loop_from_db: LoopEnum = res.scalar().loop

    # if user clicks on this button first time create task
    if loop_from_db is LoopEnum.first:
        # next_run = datetime.now(timezone.utc) + timedelta(hours=Loop1.task_1.hour)
        next_run = datetime.now(timezone.utc) + timedelta(seconds=Loop1.task_1.hour)

        sched.add_job(
            loop1_task,
            'date',
            run_date=next_run,
            id=str(user_id),
            kwargs={
                'user_id': user_id,
                'step': Loop1.task_1,
            },
            replace_existing=True,
        )

    # anyway
    await dialog_manager.start(MainWindow.gender, mode=StartMode.RESET_STACK)
