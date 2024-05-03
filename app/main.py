import os

from fastapi import FastAPI, status
from fastapi.requests import Request
import aiohttp
import logging


app = FastAPI()

@app.post("/")
async def root(request: Request):
    async with aiohttp.ClientSession() as session:
        logging.info(msg=await request.body())
        async with session.get(
                url=f'https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage?chat_id=797228719&text=privet'
        ) as responce:
            pass
    return status.HTTP_200_OK