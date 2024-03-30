import asyncio
import logging

from aiogram import Bot, Dispatcher

from aiogram_dialog import Dialog, setup_dialogs

from config_reader import config

from keyboards.dialog.windows import (
    get_main_window,

)

from handlers import (
    start,

)


async def main():
    bot = Bot(
        token=config.bot_token.get_secret_value()
    )
    dp = Dispatcher()

    dialog = Dialog(
        get_main_window()
    )
    
    setup_dialogs(dp)

    # include aiogram_dialog
    dp.include_router(dialog)

    # include other routers
    dp.include_routers(
        start.router,
    )

    await dp.start_polling(
        bot
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())