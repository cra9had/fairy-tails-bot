from datetime import timedelta, timezone, datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode

from bot.db.models import LoopEnum
from bot.db.orm import get_user_loop, change_user_loop
from bot.scheduler.loops import Loop2
from bot.scheduler.tasks import loop2_task, base_add_job
from bot.states.user import MainWindow


router = Router()


@router.callback_query(F.data == 'get_tail')
async def get_tail_callback_handler(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(MainWindow.channel_subscription, mode=StartMode.RESET_STACK)

    user_id = callback.from_user.id

    session = dialog_manager.middleware_data['session']
    sched = dialog_manager.middleware_data['sched']

    loop_from_db: LoopEnum = await get_user_loop(session, user_id)

    # if we still don`t get access to the next loops <==> if we here first time
    if loop_from_db is LoopEnum.first:
        await change_user_loop(session, user_id, new_loop=LoopEnum.second)

        next_run = datetime.now(timezone.utc) + timedelta(hours=Loop2.task_1.hour)

        base_add_job(
            sched,
            loop2_task,
            next_run,
            user_id,
            Loop2.task_1,
        )
