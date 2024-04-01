import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from aiogram_dialog import Dialog, setup_dialogs


from handlers import (
    start,

)

from keyboards.dialog.start_windows import (
    get_main_window
)

from keyboards.dialog.profile_window import (
    get_profile_window,
    get_my_tails_window,
    get_current_tail_window,
)

from keyboards.dialog.child_windows import (
    get_child_settings_window,
    get_gender_window,
    get_name_window,
    get_age_window,
    get_child_activities_window,

)

from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(
        token=os.getenv('BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode='HTML')
    )
    dp = Dispatcher()

    start_dialog = Dialog(
        get_main_window(),
    )

    dialog_tails = Dialog(
        get_child_settings_window(),
        get_gender_window(),
        get_name_window(),
        get_age_window(),
        get_child_activities_window(),
        get_current_tail_window()
    )

    dialog_profile = Dialog(
        get_profile_window(),
        get_my_tails_window()
    )

    setup_dialogs(dp)

    # include main routers 
    # MAIN ROUTER REGISTRATION MUST BE UPPER THAN AIOGRAM_DIALOG routers!
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