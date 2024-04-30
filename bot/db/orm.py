from aiogram_dialog import DialogManager
from sqlalchemy import select, ScalarResult, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import Tale, User, LoopEnum


async def create_tale(session: AsyncSession, title: str, description: str,  user_id: int):
    tale = Tale(title=title, description_prompt=description, user_id=user_id)
    session.add(tale)
    await session.commit()

    return tale.id


async def get_tale(session: AsyncSession, tale_id: int):
    tale_query = await session.execute(
        select(Tale).where(Tale.id == tale_id)
    )
    return tale_query.scalar_one_or_none()


async def save_child_settings_to_db(session: AsyncSession, *args):
    dialog_manager: DialogManager = args[1]
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


async def change_user_loop(session: AsyncSession, user_id: int, new_loop: LoopEnum):
    query = (
        update(User)
        .filter_by(tg_id=user_id)
        .values(loop=new_loop)
    )

    await session.execute(query)
    await session.commit()
