import os
from typing import Annotated

from fastapi import FastAPI, status, HTTPException
from fastapi.requests import Request
import aiohttp

from starlette.datastructures import FormData

from app.verification.prodamus_verification import ProdamusVerification

app = FastAPI()


@app.post("/")
async def root(request: Request):
    form: FormData = await request.form()

    sign = request.headers.get('Sign')

    check_sign = ProdamusVerification.verify(form, sign)

    if not check_sign:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='You don`t have an authentication token')

    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f'https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage?chat_id=797228719&text=privet'
        ) as responce:
            pass

    return status.HTTP_200_OK