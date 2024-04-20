from datetime import datetime, timezone, timedelta
from typing import Callable

from aiogram import Bot
from apscheduler_di import ContextSchedulerDecorator

from bot.keyboards.inline.tail_keyboard import get_loop1_keyboard, get_loop2_keyboard, get_episode_keyboard, \
    get_loop4_keyboard
from bot.scheduler.loops import Loop1, Loop2, Loop3, Loop4


def base_add_job(sched: ContextSchedulerDecorator, task_to_run: Callable, next_run: datetime, user_id: int, step):
    sched.add_job(
        task_to_run,
        'date',
        run_date=next_run,
        id=str(user_id),
        kwargs={
            'user_id': user_id,
            'step': step,
        },
        replace_existing=True,
    )


async def loop1_task(bot: Bot, user_id: int, scheduler: ContextSchedulerDecorator, step: Loop1) -> None:

    await bot.send_message(text=step.text, chat_id=user_id, reply_markup=get_loop1_keyboard())

    # schedule next step

    next_step = list(Loop1)[list(Loop1).index(step) + 1]  # enum can be iterated, we take next

    if next_step is Loop1.done:
        return

    new_next_run = datetime.now(timezone.utc) + timedelta(hours=next_step.hour)

    base_add_job(
        scheduler,
        loop1_task,
        new_next_run,
        user_id,
        next_step,
    )


async def loop2_task(bot: Bot, user_id: int, scheduler: ContextSchedulerDecorator, step: Loop2) -> None:

    await bot.send_message(text=step.text, chat_id=user_id, reply_markup=get_loop2_keyboard())

    # schedule next step

    # !!! WE USE THE WHOLE CLASS LOOP2 because variable `step` is not a class, it`s an instance !!!
    next_step = list(Loop2)[list(Loop2).index(step) + 1]  # enum can be iterated, we take next.

    if next_step is Loop2.done:
        return

    new_next_run = datetime.now(timezone.utc) + timedelta(hours=next_step.hour)

    base_add_job(
        scheduler,
        loop2_task,
        new_next_run,
        user_id,
        next_step,
    )


async def loop3_task(bot: Bot, user_id: int, scheduler: ContextSchedulerDecorator, step: Loop3) -> None:

    await bot.send_message(text=step.text, chat_id=user_id, reply_markup=get_episode_keyboard())

    # schedule next step

    # !!! WE USE THE WHOLE CLASS LOOP3 because variable `step` is not a class, it`s an instance !!!
    next_step = list(Loop3)[list(Loop3).index(step) + 1]  # enum can be iterated, we take next.

    if next_step is Loop3.done:
        return

    new_next_run = datetime.now(timezone.utc) + timedelta(hours=next_step.hour)

    base_add_job(
        scheduler,
        loop3_task,
        new_next_run,
        user_id,
        next_step,
    )


async def loop4_task(bot: Bot, user_id: int, scheduler: ContextSchedulerDecorator, step: Loop4) -> None:

    await bot.send_message(text=step.text, chat_id=user_id, reply_markup=get_loop4_keyboard())

    # schedule next step

    # !!! WE USE THE WHOLE CLASS LOOP4 because variable `step` is not a class, it`s an instance !!!
    next_step = list(Loop4)[list(Loop4).index(step) + 1]  # enum can be iterated, we take next.

    if next_step is Loop4.done:
        return

    new_next_run = datetime.now(timezone.utc) + timedelta(hours=next_step.hour)

    base_add_job(
        scheduler,
        loop4_task,
        new_next_run,
        user_id,
        next_step,
    )