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
                url='https://api.telegram.org/bot7175323516:AAG2dcrVeyhq5fsCgjeMmMIQv83Dh5XLpIU/sendMessage?chat_id=797228719&text=privet'
        ) as responce:
            pass
    return status.HTTP_200_OK