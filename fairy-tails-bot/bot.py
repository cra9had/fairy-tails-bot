import asyncio
import logging

from aiogram import Bot, Dispatcher

from aiogram_dialog import Dialog, setup_dialogs

from config_reader import config

from keyboards.dialog.windows import (
    get_main_window,
    get_child_settings_window,
    get_profile_window,
    get_gender_window,
    get_name_window,
    get_age_window
)

from handlers import (
    start,

)


async def main():
    bot = Bot(
        token=config.bot_token.get_secret_value()
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
    )

    dialog_profile = Dialog(
        get_profile_window()
    )

    setup_dialogs(dp)

    # include other routers 
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