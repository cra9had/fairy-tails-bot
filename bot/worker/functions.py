import logging
import os

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram_dialog import DialogManager

from arq.worker import Worker

from bot.keyboards.inline.tail_keyboard import get_tail_keyboard, get_episode_keyboard
from bot.services.tales_prompts import TaleGenerator
from bot.texts import REACHED_TALE_END

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def send_tail_plan_to_user_task(ctx: Worker, user_id: int, context: dict | None = None):
    bot: Bot = ctx['bot']
    tale_plan = context.get('tale_plan', 'NoPlanForTale')
    async with bot.session:
        await bot.send_message(
            text=tale_plan,
            parse_mode=ParseMode.HTML,
            chat_id=user_id,
            reply_markup=get_tail_keyboard()
        )

    return f'Sent plan to user {user_id} successfully'


async def send_tail_to_user_task(ctx: Worker, user_id: int, context: dict):
    bot: Bot = ctx['bot']
    tale = context.get('tale', 'NoTale')
    finish = context.get('finish')
    if finish:
        markup = None
        msg_text = tale
    else:
        markup = get_episode_keyboard()
        msg_text = tale
    async with bot.session:
        await bot.send_message(
            text=msg_text,
            chat_id=user_id,
            reply_markup=markup
        )

    return f'Sent tail to user {user_id} successfully'


async def send_episode_to_user_task(ctx: Worker, user_id: int):
    bot: Bot = ctx['bot']
    async with bot.session:
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
