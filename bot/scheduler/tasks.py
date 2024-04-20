from aiogram import Bot


async def test_task(bot: Bot, user_id: int):
    async with bot.session:
        await bot.send_message(text='TEST!!', chat_id=user_id)
