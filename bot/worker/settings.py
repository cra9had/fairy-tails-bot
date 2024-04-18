import os

from arq.connections import RedisSettings
from dotenv import  load_dotenv
from bot.worker.functions import sample_background_task, shutdown, startup

load_dotenv(dotenv_path='.env')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))


class WorkerSettings:
    functions = [sample_background_task]
    redis_settings = RedisSettings(host=REDIS_HOST, port=REDIS_PORT)
    on_startup = startup
    on_shutdown = shutdown
    handle_signals = False

