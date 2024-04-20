from datetime import datetime, timezone, timedelta

from aiogram import Bot
from apscheduler_di import ContextSchedulerDecorator

from bot.scheduler.loops import Loop1


async def loop1_task(bot: Bot, user_id: int, scheduler: ContextSchedulerDecorator, step: Loop1) -> None:
    await bot.send_message(text=step.text, chat_id=user_id)

    # schedule next step

    next_step = list(Loop1)[list(Loop1).index(step) + 1]  # enum can be iterated, we take next

    if next_step is Loop1.done:
        return

    calculated_next_run = datetime.now(timezone.utc) + timedelta(seconds=next_step.hour)
    scheduler.add_job(
        loop1_task,
        'date',
        run_date=calculated_next_run,
        id=str(user_id),
        kwargs={
            'user_id': user_id,
            'step': next_step,
        },
        replace_existing=True,
    )
