import asyncio
import logging
import os

import requests
import json

from dotenv import load_dotenv
from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

logger = logging.getLogger(__name__)

load_dotenv(dotenv_path='.env')

HEADERS = {
    'Authorization': f'Bearer {os.getenv("TRANSLATION_API_KEY")}',
    'Content-Type': 'application/json'
}

SYNTHESIZE_URL = 'https://apihost.ru/api/v1/synthesize'
PROCESS_URL = 'https://apihost.ru/api/v1/process'


async def send_to_translation(text: str, user_id: int):
    logging.info(f'Sending user_id {user_id} text to translate: {text}')
    data = {
        'data': [{
            'lang': 'ru-RU',
            'speaker': '5010',
            'emotion': 'good',
            'text': text,
            'rate': '0.9',
            'pitch': '1.0',
            'type': 'mp3',
            'pause': '5'
        }]
    }

    json_data = json.dumps(data)

    response = requests.post(SYNTHESIZE_URL, headers=HEADERS, data=json_data)
    if response.status_code == 200:
        process = response.json().get('process')
        if not process:
            raise RuntimeError(f"No process key in response json {response.json()}")
        return response.json()['process']
    else:
        logging.error(f'Bad Translation-API Response. Check TRANSLATION_API_KEY or API balance')
        raise RuntimeError("Bad response in send_to_translation: check TRANSLATION_API_KEY in env")


async def get_link_translation(process_id: str, user_id: int):
    data = {'process': process_id}
    json_data = json.dumps(data)
    request_counter = 0
    while True:
        logging.info(f'Voice-Translation request №{request_counter} of user_id {user_id}:')

        if request_counter > 10:
            raise RuntimeError(
                "Too long for usual loading voice-translation. You can adjust timeout in bot/services/text_to_speech.py")
        response = requests.post(PROCESS_URL, headers=HEADERS, data=json_data)

        if response.json()['status'] != 205:
            break

        logging.info(f'Voice-Translation request №{request_counter} isn\'t ready yet. Will try again in 5 seconds.')
        await asyncio.sleep(5)
        request_counter += 1

    return response.json()['message']


async def process_translation(text: str, user_id: int):
    try:
        logging.info(f'Processing user {user_id} text to translation')
        #order_id = await send_to_translation(text, user_id)
        #voice_msg_url = await get_link_translation(order_id, user_id)
        voice_msg_url = 'http://commondatastorage.googleapis.com/codeskulptor-assets/Collision8-Bit.ogg'
        return MediaAttachment(type=ContentType.AUDIO, url=voice_msg_url)
    except RuntimeError as e:
        logging.error(f'Something\'s wrong with voice translation: {e}')
