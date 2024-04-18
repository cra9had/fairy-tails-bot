import logging
import os

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from arq.worker import Worker


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def send_tail_to_user_task(ctx: Worker, user_id: int):
    bot: Bot = ctx['bot']

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ПОЛУЧИТЬ СКАЗКУ', callback_data='get_tail')]])

    async with bot.session:
        await bot.send_message(chat_id=user_id, text='Task is ended', reply_markup=keyboard)


    return f'Sent tail to user {user_id} successfully'


async def startup(ctx: Worker) -> None:
    ctx['bot'] = Bot(os.getenv('BOT_TOKEN'))
    logging.info("Worker Started")


async def shutdown(ctx: Worker) -> None:
    logging.info("Worker end")
