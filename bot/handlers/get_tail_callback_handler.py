import logging
from datetime import timedelta, timezone, datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode, ShowMode

from bot.db.models import LoopEnum
from bot.db.orm import get_user_loop, change_user_loop
from bot.scheduler.loops import Loop2
from bot.scheduler.tasks import loop2_task, base_add_job
from bot.states.user import MainWindow

router = Router()

logger = logging.getLogger(__name__)

@router.callback_query(F.data == 'get_tail')
async def get_tail_callback_handler(callback: CallbackQuery, dialog_manager: DialogManager):
    print("GET_TAIL:", dialog_manager.dialog_data)

    chat_history = dialog_manager.dialog_data.get('chat_history')
    tale_params = dialog_manager.dialog_data.get('tale_params')

    await dialog_manager.start(MainWindow.channel_subscription, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND,
                               data={"tale_params": tale_params, "chat_history": chat_history})
    dialog_manager.middleware_data.update({"tale_params": tale_params, "chat_history": chat_history})

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
    await callback.answer()