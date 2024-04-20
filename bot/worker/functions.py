import logging
import os

from aiogram import Bot

from arq.worker import Worker

from bot.db.orm import get_current_episode_index
from bot.keyboards.inline.tail_keyboard import get_tail_keyboard, get_episode_keyboard


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def send_tail_to_user_task(ctx: Worker, user_id: int):
    bot: Bot = ctx['bot']
    async with bot.session:
        await bot.send_photo(
            chat_id=user_id,
            photo='https://www.storyberries.com/wp-content/uploads/2019/01/Bedtime-stories-Snow-White-and-the-Seven-Dwarves-fairy-tales-for-kids.jpg',
            caption='Содержание сезона',
            reply_markup=get_tail_keyboard()
        )

    return f'Sent tail to user {user_id} successfully'


async def send_episode_to_user_task(ctx: Worker, user_id: int, current_tail_index: int):
    bot: Bot = ctx['bot']

    async with bot.session:
        await bot.send_message(user_id, text=f'Серия номер {current_tail_index}')

        await bot.send_audio(
            chat_id=user_id,
            audio='https://web-skazki.ru/audio-files/luntik.mp3',
            reply_markup=get_episode_keyboard()
        )

    return f'Sent episode to user {user_id} successfully'

async def startup(ctx: Worker) -> None:
    ctx['bot'] = Bot(os.getenv('BOT_TOKEN'))
    logging.info("Worker Started")


async def shutdown(ctx: Worker) -> None:
    logging.info("Worker end")
