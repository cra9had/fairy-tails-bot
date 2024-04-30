import asyncio
import os

import requests
import json

from dotenv import load_dotenv
from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

load_dotenv(dotenv_path='.env')

HEADERS = {
    'Authorization': f'Bearer {os.getenv("TRANSLATION_API_KEY")}',
    'Content-Type': 'application/json'
}

SYNTHESIZE_URL = 'https://apihost.ru/api/v1/synthesize'
PROCESS_URL = 'https://apihost.ru/api/v1/process'


async def send_to_translation(text: str):
    data = {
        'data': [{
            'lang': 'ru-RU',
            'speaker': '1011',
            'emotion': 'neutral',
            'text': text,
            'rate': '1.0',
            'pitch': '1.0',
            'type': 'mp3',
            'pause': '0'
        }]
    }

    json_data = json.dumps(data)

    response = requests.post(SYNTHESIZE_URL, headers=HEADERS, data=json_data)
    if response.status_code == 200:
        return response.json()['process']
    else:
        print(response.json())
        raise RuntimeError("Bad response in send_to_translation: check TRANSLATION_API_KEY in env")


async def get_link_translation(process_id: str):
    data = {'process': process_id}
    json_data = json.dumps(data)
    request_counter = 0
    while True:
        if request_counter > 10:
            raise RuntimeError(
                "Too long for usual loading voice-translation. You can adjust timeout in bot/services/text_to_speech.py")
        print(f"Отправка запроса на получение результата {process_id}..")
        response = requests.post(PROCESS_URL, headers=HEADERS, data=json_data)
        if response.json()['status'] == 205:
            print("Результат пока ещё не готов. Попробую снова через 5 секунд..")
            await asyncio.sleep(5)
            request_counter += 1
            continue
        else:
            break

    return response.json()['message']


async def process_translation(text: str):
    order_id = await send_to_translation(text)
    voice_msg_url = await get_link_translation(order_id)
    return MediaAttachment(type=ContentType.AUDIO, url=voice_msg_url)
