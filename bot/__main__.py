import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import Dialog, setup_dialogs
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from bot.db.models import Base
from bot.handlers import start
from bot.getters.user import get_full_info_for_dialog
from bot.keyboards.dialog.start_windows import get_main_window, get_more_info_window
from bot.keyboards.dialog.profile_window import (get_profile_window, get_my_tails_window,
                                                 get_current_tail_window, get_episode_ended_window,
                                                 get_my_subscriptions_window)

from bot.keyboards.dialog.buy_subscription import (get_buy_subscription,
                                                   get_user_dont_have_subsription)

from bot.keyboards.dialog.child_windows import (get_child_settings_window,
                                                get_gender_window, get_name_window,
                                                get_age_window, get_child_activities_window)

from bot.keyboards.dialog.tail_window import get_descr_tail_window, get_chapter_window

from bot.middlewares.user.check_user_subscription import CheckUserSubscription
from bot.middlewares.db import DbSessionMiddleware

load_dotenv(dotenv_path='.env')


async def main():
    engine = create_async_engine(os.getenv('DB_URL'), future=True, echo=True)
    db_pool = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(
        token=os.getenv('BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode='HTML')
    )

    dp = Dispatcher()

    dp.callback_query.middleware(CheckUserSubscription())

    start_dialog = Dialog(
        get_main_window(),
        get_more_info_window(),
        on_start=get_full_info_for_dialog
    )

    dialog_tails = Dialog(
        get_user_dont_have_subsription(),
        get_child_settings_window(),
        get_gender_window(),
        get_name_window(),
        get_current_tail_window(),
        get_age_window(),
        get_child_activities_window(),
        get_episode_ended_window(),
        get_descr_tail_window(),
        get_chapter_window(),
        on_start=get_full_info_for_dialog
    )

    dialog_profile = Dialog(
        get_profile_window(),
        get_my_tails_window(),
        get_buy_subscription(),
        get_my_subscriptions_window(),
        on_start=get_full_info_for_dialog
    )

    setup_dialogs(dp)

    # include main routers 
    # MAIN ROUTER REGISTRATION MUST BE UPPER THAN AIOGRAM_DIALOG routers!
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(DbSessionMiddleware(db_pool))

    dp.include_routers(
        start.router,

    )

    # include aiogram_dialogs
    dp.include_routers(
        start_dialog,
        dialog_profile,
        dialog_tails
    )

    await dp.start_polling(
        bot
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
