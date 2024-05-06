import os
from aiogram import Bot, html
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from fastapi import FastAPI, status, HTTPException
from fastapi.requests import Request
import aiohttp

from starlette.datastructures import FormData

from app.verification.prodamus_verification import ProdamusVerification
from bot.db.db_pool import db_pool
from bot.db.orm import change_user_chapters

app = FastAPI()
bot = Bot(token=os.getenv('BOT_TOKEN'))

@app.post("/")
async def root(request: Request):
    form: FormData = await request.form()

    sign = request.headers.get('Sign')

    tg_user_id = int(form['order_num'])
    order_sum = form['sum']

    check_sign = ProdamusVerification.verify(form, sign)

    if not check_sign:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='You don`t have an authentication token')

    elif form['payment_status'] != 'success':
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED)

    chap_quantity = 5
    async with db_pool() as session:
        await change_user_chapters(session, tg_user_id, chap_quantity)

    async with bot.session:
        kb = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(
                    text='Сгенерировать сказку',
                    callback_data='generate_tail_from_subscription_window'
                )]]
            )

        await bot.send_message(tg_user_id, f'Успешная оплата.\nСумма платежа {html.bold(order_sum)} рублей',
                               reply_markup=kb, parse_mode='HTML')
        await bot.send_sticker(tg_user_id, sticker='CAACAgIAAxkBAAEMDhRmN0QZVQRuIW8_Li6jkGPQEQ8q2AAC7QIAAvPjvguyApHPzINUljUE')

    return status.HTTP_200_OK