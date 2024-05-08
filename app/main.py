import os
import math
from aiogram import Bot, html
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from fastapi import FastAPI, status, HTTPException
from fastapi.requests import Request
import aiohttp

from starlette.datastructures import FormData

from app.db.orm import update_plan, set_loop_subscriber
from app.verification.prodamus_verification import ProdamusVerification
from bot.db.db_pool import db_pool
from bot.db.orm import change_user_chapters, update_user_segment

from bot.db.models import SubscriptionEnum, SegmentEnum


app = FastAPI()
bot = Bot(token=os.getenv('BOT_TOKEN'))

@app.post("/")
async def root(request: Request):
    form: FormData = await request.form()

    sign = request.headers.get('Sign')

    tg_user_id = int(form['order_num'])
    order_sum = math.trunc(float(form['sum']))

    check_sign = ProdamusVerification.verify(form, sign)

    if not check_sign:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='You don`t have an authentication token')

    elif form['payment_status'] != 'success':
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED)

    match order_sum:
        case 690:
            chap_quantity = 10
            subscription_plan = SubscriptionEnum.min_plan
        case 1090:
            chap_quantity = 20
            subscription_plan = SubscriptionEnum.standard_plan
        case 1190:
            chap_quantity = 30
            subscription_plan = SubscriptionEnum.max_plan

    async with db_pool() as session:
        await change_user_chapters(session, tg_user_id, chap_quantity)
        await update_plan(session=session, subscription_plan=subscription_plan, tg_id=tg_user_id)
        await set_loop_subscriber(session=session, tg_id=tg_user_id)
        await update_user_segment(tg_id=tg_user_id, segment=SegmentEnum.payed)

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