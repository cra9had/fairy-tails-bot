from typing import Optional

from aiogram import Bot
from aiogram.types import CallbackQuery, User
from aiogram.types.input_file import URLInputFile

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.orm import create_tale
from bot.states.user import Tail, Profile, MainWindow


async def to_profile(*args):
    dialog_manager: DialogManager = args[2]
    await dialog_manager.start(state=Profile.my_profile, mode=StartMode.RESET_STACK)


async def to_start(*args):
    dialog_manager: DialogManager = args[2]
    await dialog_manager.start(state=MainWindow.start, mode=StartMode.RESET_STACK)


async def to_child(*args):
    dialog_manager: DialogManager = args[2]
    await dialog_manager.start(state=Tail.all_child_settings, mode=StartMode.RESET_STACK)


async def to_buy_subscription(*args):
    dialog_manager: DialogManager = args[2]
    await dialog_manager.start(Profile.subscription, mode=StartMode.RESET_STACK)


async def buy_new_tail(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs
):
    user_subscribed: bool = dialog_manager.middleware_data['user_subscribed']
    if not user_subscribed:
        await dialog_manager.switch_to(Tail.user_dont_have_subscription)

    tale_plan = dialog_manager.dialog_data.get('tale_plan')
    tale_title = dialog_manager.dialog_data.get('tale_title')
    session = dialog_manager.dialog_data.get('session')

    await create_tale(session, tale_title, tale_plan, callback.message.chat.id)

    await to_start(None, None, dialog_manager)
    await callback.message.answer('Ваша сказка успешно куплена и находится у вас в профиле!')
    await callback.message.answer_sticker('CAACAgIAAxkBAAEL1JxmC9SQJqwO9gX45wri2B5vw0lVLwAChAADpsrIDDCcD7Wym5gUNAQ')


async def send_audio_file(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    bot: Bot = dialog_manager.middleware_data['bot']
    user: User = dialog_manager.middleware_data['event_from_user']

    await bot.send_audio(chat_id=user.id, audio='https://web-skazki.ru/audio-files/luntik.mp3')


async def check_user_setted(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data[
        'from_child_settings'] = True  # because we can't continue tail from this window, only start new one
    all_settings = {"gender", "name", "age", "activities"}
    setted: bool = (all_settings & dialog_manager.dialog_data.keys()) == all_settings

    if setted:
        await dialog_manager.switch_to(Tail.tail)

    elif not dialog_manager.dialog_data.get("can_send_data"):
        await callback.answer("Вы должны заполнить все поля", show_alert=True)
        return


# ----------------------SETTERS----------------------


async def set_child_activities(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    # HERE SOME LOGIC TO SET CHILD ACTUAL ACTIVITY TO DATABASE
    dialog_manager.dialog_data["activities"] = button.text.text
    await callback.answer("Увлечения установлены")
    # return user back to menu
    await dialog_manager.switch_to(Tail.all_child_settings)


async def set_child_gender(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    # HERE SOME LOGIC TO SET CHILD ACTUAL GENDER TO DATABASE
    dialog_manager.dialog_data["gender"] = button.text.text
    await callback.answer("Пол установлен")
    # return user back to menu
    await dialog_manager.switch_to(Tail.all_child_settings)


async def set_child_age(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    # HERE SOME LOGIC TO SET CHILD ACTUAL AGE TO DATABASE
    dialog_manager.dialog_data["age"] = button.widget_id
    await callback.answer("Возраст установлен")
    # return user back to menu
    await dialog_manager.switch_to(Tail.all_child_settings)
