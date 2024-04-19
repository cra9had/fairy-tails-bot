import os
import asyncio
import logging

from redis.asyncio import Redis

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import Dialog, setup_dialogs
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

from bot.db.models import Base
from bot.handlers import get_tail_callback_handler, start, get_next_episode_callback_handler
from bot.getters.user import get_full_info_for_dialog


from bot.keyboards.dialog.main_windows import get_gender_window, get_age_window, get_child_activities_window, \
    get_name_window, get_child_settings_window, get_waiting_tail_window, get_channel_subscription_window, \
    get_waiting_episode_window
from bot.keyboards.dialog.subscription_windows import get_discount_text_window, get_subscription_plans_window, \
    get_buy_subscription_window

from bot.middlewares.user.check_user_subscription import CheckUserSubscription
from bot.middlewares.db import DbSessionMiddleware
from bot.middlewares.user.episode_and_tail_indexes import EpisodeAndTailIndexesMiddleware

load_dotenv(dotenv_path='.env')


async def main():
    engine = create_async_engine(os.getenv('DB_URL'), future=True, echo=True)
    db_pool = async_sessionmaker(engine, expire_on_commit=False)

    arq_pool: ArqRedis = await create_pool(
        RedisSettings(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
        )
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(
        token=os.getenv('BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode='HTML'),
    )

    dp = Dispatcher(
        storage=RedisStorage(
            Redis(
                host=os.getenv('REDIS_HOST'),
                port=int(os.getenv('REDIS_PORT'))
            ),
            key_builder=DefaultKeyBuilder(with_destiny=True)
        ),
        arq_pool=arq_pool,
    )

    dialog_tails = Dialog(
        get_gender_window(),
        get_age_window(),
        get_child_activities_window(),
        get_name_window(),
        get_child_settings_window(),
        get_waiting_tail_window(),
        get_channel_subscription_window(),
        get_waiting_episode_window(),

        on_start=get_full_info_for_dialog
    )

    dialog_subscription = Dialog(
        get_discount_text_window(),
        get_subscription_plans_window(),
        get_buy_subscription_window(),
    )

    setup_dialogs(dp)

    # include main routers
    # MAIN ROUTER REGISTRATION MUST BE UPPER THAN AIOGRAM_DIALOG routers!
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(CheckUserSubscription())

    dialog_tails.callback_query.middleware(EpisodeAndTailIndexesMiddleware())

    dp.include_routers(
        start.router,
        get_tail_callback_handler.router,
        get_next_episode_callback_handler.router,
    )

    # include aiogram_dialogs
    dp.include_routers(
        dialog_tails,
        dialog_subscription,
    )

    await dp.start_polling(
        bot
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
