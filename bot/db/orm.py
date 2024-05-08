import logging
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy import select, ScalarResult, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import Tale, User, LoopEnum

from bot.states.user import Subscription

from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


async def add_user(session: AsyncSession, tg_id: int, username: str | None = None):
    user_query = await session.execute(select(User).filter_by(tg_id=tg_id))
    existing_user = user_query.scalar_one_or_none()

    if existing_user:
        logger.info(f"User {tg_id} already exists")
        return existing_user

    try:
        if username:
            new_user = User(tg_id=tg_id, username=username)
        else:
            new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        logger.info(f"User {tg_id} has been added into users table")
        return new_user
    except IntegrityError as e:
        logger.error(f"While adding user {tg_id} into users table occurs IntegrityError: {e}")
        await session.rollback()


async def change_user_chapters(session: AsyncSession, tg_id: int, chap_quantity: int | None = 1):
    """
    Add chapters for a user with the given tg_id.

    :param session: AsyncSession object for database interaction.
    :param tg_id: Telegram ID of the user.
    :param chap_quantity: Number of chapters to add.
    """
    user = await session.execute(select(User).filter_by(tg_id=tg_id))
    user = user.scalar_one_or_none()

    if user:
        user.chapters_available += chap_quantity
        await session.commit()
    else:
        logger.error(f"Cannot change chapters for User {tg_id}: not found")
        await session.rollback()


async def get_user_chapters(session: AsyncSession, tg_id: int):
    user = await session.execute(select(User).filter_by(tg_id=tg_id))
    user = user.scalar_one_or_none()

    if user:
        return user.chapters_available


async def create_tale(session: AsyncSession, title: str, description: str, user_id: int):
    tale = Tale(title=title, description_prompt=description, user_id=user_id)
    session.add(tale)
    await session.commit()

    return tale.id


async def get_tale(session: AsyncSession, tale_id: int):
    tale_query = await session.execute(
        select(Tale).where(Tale.id == tale_id)
    )
    return tale_query.scalar_one_or_none()


async def save_child_settings_to_db(*args):
    dialog_manager: DialogManager = args[2]
    user_id = dialog_manager.event.from_user.id
    username = dialog_manager.event.from_user.username

    session: AsyncSession = dialog_manager.middleware_data['session']

    user = await add_user(session, user_id, username)

    if not user.chapters_available:
        await dialog_manager.start(Subscription.discount, mode=StartMode.RESET_STACK)
    # logic to save all settings to db


async def get_user_have_sub(session: AsyncSession, user_id: int):
    return False  # FOR TEST!!
    # logic to check user have subscription


async def get_current_episode_index(session: AsyncSession, user_id: int):
    return 1  # FOR TEST!!
    # logic to check user`s last episode number


async def get_current_tail_index(session: AsyncSession, user_id: int):
    return 1  # FOR TEST!!
    # logic to check user`s last tail index (season)


async def get_user_loop(session: AsyncSession, user_id: int):
    res = await session.execute(select(User).filter_by(tg_id=user_id))

    loop_from_db: LoopEnum = res.scalar().loop

    return loop_from_db


async def get_user(session: AsyncSession, user_id: int):
    res = await session.execute(select(User).filter_by(tg_id=user_id))

    user_from_db = res.scalar_one_or_none()
    return user_from_db


async def change_user_loop(session: AsyncSession, user_id: int, new_loop: LoopEnum):
    query = (
        update(User)
        .filter_by(tg_id=user_id)
        .values(loop=new_loop)
    )

    await session.execute(query)
    await session.commit()


async def update_tale_data():
    pass
