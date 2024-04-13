from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import Tale


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
