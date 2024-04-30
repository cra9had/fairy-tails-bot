import logging
import os

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import URLInputFile
from arq.worker import Worker

from bot.keyboards.inline.tail_keyboard import get_tail_keyboard, get_episode_keyboard
from bot.texts.window_texts import REACHED_TALE_END, NEXT_EPISODE_READY_TO_BE_LOADED

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def send_tail_plan_to_user_task(ctx: Worker, user_id: int, context: dict | None = None):
    bot: Bot = ctx['bot']
    tale_photo = URLInputFile(context.get('tale_photo_url'))
    async with bot.session:
        await bot.send_photo(
            chat_id=user_id,
            photo=tale_photo,
            caption='Чтобы получить вашу сказку - нажмите на кнопку!',
            reply_markup=get_tail_keyboard()
        )

    return f'Sent plan to user {user_id} successfully'


async def send_tail_to_user_task(ctx: Worker, user_id: int, context: dict):
    bot: Bot = ctx['bot']
    finish = context.get('finish')
    if finish:
        markup = None
        msg_text = REACHED_TALE_END
    else:
        markup = get_episode_keyboard()
        msg_text = NEXT_EPISODE_READY_TO_BE_LOADED
    async with bot.session:
        await bot.send_message(
            text=msg_text,
            chat_id=user_id,
            reply_markup=markup
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
