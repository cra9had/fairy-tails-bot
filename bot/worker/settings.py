import os

from arq.connections import RedisSettings
from dotenv import load_dotenv, find_dotenv
from bot.worker.functions import shutdown, startup, send_tail_to_user_task, send_episode_to_user_task, \
    send_tail_plan_to_user_task

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))

load_dotenv(find_dotenv())


class WorkerSettings:
    functions = [send_tail_to_user_task, send_episode_to_user_task, send_tail_plan_to_user_task]
    redis_settings = RedisSettings(host=REDIS_HOST, port=REDIS_PORT)
    on_startup = startup
    on_shutdown = shutdown
    handle_signals = False

