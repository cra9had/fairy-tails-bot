import asyncio
from datetime import datetime, timezone, timedelta
from pprint import pprint
from typing import Optional
from aiogram import html, Bot
from aiogram.types import Message, CallbackQuery
from apscheduler_di import ContextSchedulerDecorator

from arq import ArqRedis

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import DialogManager, StartMode, ShowMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import LoopEnum, TaleParams
from bot.db.orm import get_current_tail_index, get_current_episode_index, get_user_loop, change_user_loop, get_user, \
    change_user_chapters, add_user
from bot.on_clicks.user import to_child, to_profile, to_start, to_buy_subscription
from bot.payments.generate_payment_link import GeneratePaymentLinkFabric
from bot.scheduler.loops import Loop1, Loop3, Loop4
from bot.states.user import Subscription
from bot.scheduler.tasks import base_add_job, loop3_task, loop4_task
from bot.services.gpt import ChatGPT
from bot.services.tales_prompts import TaleGenerator
from bot.services.text_to_speech import process_translation
from bot.texts.window_texts import WAIT_GENERATION_TALE, TIP_TEXT, WAIT_GENERATION_PLAN, NEXT_EPISODE_GENERATION

from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId


async def get_plans(**kwargs):
    plans = [
        ('Минимальный', 690),
        ('Стандартный', 1090),
        ('Максимальный', 1190),
    ]

    return {
        "plans": plans,
    }


async def get_payment_url(dialog_manager: DialogManager, **kwargs):
    payment_fabric: GeneratePaymentLinkFabric = dialog_manager.middleware_data['payment_fabric']

    plan = dialog_manager.dialog_data['plan_selected']

    payment_url = await payment_fabric.generate_payment_link(
        price=plan,
        order_id=dialog_manager.event.from_user.id
    )

    return {
        'payment_url': payment_url,
    }


async def get_full_info_for_dialog(*args, **kwargs):
    dialog_manager: DialogManager = args[1]

    user_child_settings = {}  # LOAD USER SETTED SETTING HERE FROM DATABASE!

    # LOAD USER TAILS HERE FROM DATABASE!
    data = {
        'user_child_settings': user_child_settings,
    }

    # upload all collected settings to dialog
    dialog_manager.dialog_data.update(data)


async def get_setted_child_settings(dialog_manager: DialogManager, **kwargs):
    gender = dialog_manager.dialog_data.get('gender')
    name = dialog_manager.dialog_data.get('name')
    age = dialog_manager.dialog_data.get('age')
    activities = dialog_manager.dialog_data.get('activities')
    return {
        'gender': gender,
        'name': name,
        'age': age,
        'activities': activities,
    }


async def create_task_to_plan(arq_pool: ArqRedis, dialog_manager: DialogManager, event_update,
                              **kwargs):
    user_id: int = dialog_manager.event.from_user.id

    message = await event_update.callback_query.message.answer(WAIT_GENERATION_PLAN)
    await event_update.callback_query.message.delete()
    await event_update.callback_query.answer()

    data = await get_setted_child_settings(dialog_manager, **kwargs)
    start_data = dialog_manager.start_data
    sex, name, age, interests = data["gender"], data["name"], data["age"], data["activities"]

    if start_data:
        chat_history = start_data.get('chat_history')
        tale_params = start_data.get('tale_params')
        if tale_params:
            dialog_manager.dialog_data.update(tale_params=tale_params)
    else:
        chat_history = tale_params = None

    tg = TaleGenerator()
    if not tale_params:
        tale_plan = await tg.generate_tale_plan(sex=sex, name=name, age=age, interests=interests)
    else:
        tale_plan = await tg.generate_tale_plan_continue(provided_history=chat_history)

    tale_photo_url = await tg.generate_tale_season_photo(season_plan=tale_plan)
    dialog_manager.dialog_data.update(tale_plan=tale_plan)
    dialog_manager.dialog_data.update(chat_history=tg.gpt.discussion[:])

    user_id: int = dialog_manager.event.from_user.id

    await message.delete()
    await arq_pool.enqueue_job('send_tail_plan_to_user_task',
                               user_id=user_id, context={"tale_photo_url": tale_photo_url})

    return {"tale_plan": tale_plan, 'tale_photo_url': tale_photo_url}


async def create_task_to_tail(arq_pool: ArqRedis, dialog_manager: DialogManager, event_update, session,
                              sched: ContextSchedulerDecorator, **kwargs):
    user_id: int = dialog_manager.event.from_user.id
    username = dialog_manager.event.from_user.username

    user = await add_user(session, user_id, username)

    if not user.chapters_available:
        await dialog_manager.start(Subscription.discount, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)
        return

    # to start 3-thd scheduling
    await create_task_to_episode(sched=sched, arq_pool=arq_pool, dialog_manager=dialog_manager,
                                 event_update=event_update, session=session)

    data = dialog_manager.start_data
    provided_history = data.get('chat_history') or []
    tale_params = TaleParams.from_json(data.get('tale_params')) if data.get('tale_params', None) else TaleParams()

    tg = TaleGenerator(provided_history=provided_history)
    if tale_params.is_season_begin():
        await event_update.callback_query.message.answer(WAIT_GENERATION_TALE)
        tale = await tg.generate_first_chapter(tale_params.season)
    else:
        await event_update.callback_query.message.answer(NEXT_EPISODE_GENERATION)
        tale = await tg.generate_next_chapter()

    await change_user_chapters(session, user_id, -1)
    tale_voice = await process_translation(text=tale, user_id=user_id)

    finish = False
    try:
        tale_params.iterate()
    except StopIteration:
        finish = True

    dialog_manager.dialog_data.update({"tale_params": tale_params.to_json(), "chat_history": tg.gpt.discussion[:]})
    await arq_pool.enqueue_job('send_tail_to_user_task', user_id=user_id,
                               context={"finish": finish})

    return {"tale_voice": tale_voice}


async def create_schedule_loop4(
        dialog_manager: DialogManager,
        sched: ContextSchedulerDecorator,
        **kwargs
):
    session: AsyncSession = dialog_manager.middleware_data['session']

    await change_user_loop(session=session, user_id=dialog_manager.event.from_user.id, new_loop=LoopEnum.fourth)

    user_id: int = dialog_manager.event.from_user.id

    next_run = datetime.now(timezone.utc) + timedelta(hours=Loop4.task_1.hour)

    base_add_job(
        sched,
        loop4_task,
        next_run,
        user_id,
        Loop4.task_1,
    )

    return {}  # to don`t catch an exception


async def create_task_to_episode(
        arq_pool: ArqRedis,
        dialog_manager: DialogManager,
        sched: ContextSchedulerDecorator,
        session: AsyncSession,
        **kwargs
):
    user_id: int = dialog_manager.event.from_user.id

    session = dialog_manager.middleware_data['session']

    # for the future
    # current_tail_index: int = await get_current_tail_index(session, user_id)
    #
    # await arq_pool.enqueue_job('send_episode_to_user_task', user_id=user_id, current_tail_index=current_tail_index)

    loop_from_db: LoopEnum = await get_user_loop(session, user_id)

    if loop_from_db is not LoopEnum.subscriber and loop_from_db is LoopEnum.second:
        await change_user_loop(session, user_id, LoopEnum.third)

        next_run = datetime.now(timezone.utc) + timedelta(hours=Loop3.task_1.hour)

        base_add_job(
            sched,
            loop3_task,
            next_run,
            user_id,
            Loop3.task_1,
        )

    return {}  # to don`t catch an exception


async def get_fullname(
        event_from_user: Message, dialog_manager: DialogManager, **kwargs
):
    safe_bold_full_name = html.bold(html.quote(event_from_user.full_name))
    return {
        'full_name': safe_bold_full_name
    }


async def get_my_tails(
        dialog_manager: DialogManager, **kwargs
):
    current_tail_index: int = dialog_manager.dialog_data.get('current_tail_index', 1)
    max_pages: int = dialog_manager.dialog_data['max_pages']
    current_tail: str = dialog_manager.dialog_data['tails'].get(current_tail_index)

    data = {
        'current_tail_index': current_tail_index,
        'max_pages': max_pages,
        'current_tail': current_tail
    }

    return data


async def get_current_tail(
        event_from_user: CallbackQuery, dialog_manager: DialogManager, **kwargs
):
    # number of the choosen tail from pagination
    current_tail_index = dialog_manager.start_data['current_tail_index']

    # GET something about episode: text, name, maybe short description FROM DATABASE
    current_episode_index: int = dialog_manager.dialog_data['current_episode_index']
    current_episode_text = dialog_manager.dialog_data['tails'][current_tail_index]['name']

    season = dialog_manager.dialog_data['tails'][current_tail_index][
        'season']  # ('SELECT season FROM tails WHERE tail_index == ?', (current_tail_index, ))

    # GET file_id for current episode or link or smth else FROM DATABASE
    photo_for_episode = 'https://i0.wp.com/mynintendonews.com/wp-content/uploads/2019/09/fairy_tail.jpg?resize=930%2C620&ssl=1'

    return {
        'season': season,
        'photo': photo_for_episode,
        'current_tail_index': current_tail_index,
        'current_episode_index': current_episode_index,
        'current_episode_text': current_episode_text,
    }


async def get_generated_plan_and_photo(
        event_from_user: CallbackQuery, dialog_manager: DialogManager, session: AsyncSession, **kwargs
):
    if dialog_manager.dialog_data['from_child_settings']:
        season = 1
        episode = 1
        tale_generator = TaleGenerator()

    else:
        current_tail_index = dialog_manager.dialog_data['current_tail_index']
        season = dialog_manager.dialog_data['tails'][current_tail_index]['season'] + 1
        tale_generator = dialog_manager.dialog_data['tale_generator'] or TaleGenerator()

    tale_plan = await tale_generator.generate_tale_plan(name=dialog_manager.dialog_data.get("name"),
                                                        sex=dialog_manager.dialog_data.get("gender"),
                                                        age=dialog_manager.dialog_data.get("age"),
                                                        interests=dialog_manager.dialog_data.get("activities")
                                                        )

    tale_title = await tale_generator.generate_tale_title()

    dialog_manager.dialog_data.update({'tale_plan': tale_plan,
                                       'tale_title': tale_title,
                                       'session': session,
                                       'season': season,
                                       'tale_generator': tale_generator})

    return {
        'season': season,
        'tale_plan': tale_plan,
    }
