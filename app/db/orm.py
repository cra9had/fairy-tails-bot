from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import SubscriptionEnum, User, LoopEnum


async def set_loop_subscriber(session: AsyncSession, tg_id: int) -> None:
    query = (
        update(User)
        .values(
            loop=LoopEnum.subscriber
        )
        .where(User.tg_id == tg_id)
    )

    await session.execute(query)
    await session.commit()


async def update_plan(session: AsyncSession, subscription_plan: SubscriptionEnum, tg_id: int) -> None:
    query = (
        update(User)
        .values(
            subscription_plan=subscription_plan
        )
        .where(User.tg_id == tg_id)
    )

    await session.execute(query)
    await session.commit()
