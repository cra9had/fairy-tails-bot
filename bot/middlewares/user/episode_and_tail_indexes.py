from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.db.orm import get_user_have_sub, get_current_episode_index, get_current_tail_index


class EpisodeAndTailIndexesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session = data['session']
        user_id = event.from_user.id

        current_tail_index = await get_current_tail_index(session, user_id)
        current_episode_index = await get_current_episode_index(session, user_id)

        data['current_tail_index'] = current_tail_index
        data['current_episode_index'] = current_episode_index

        return await handler(event, data)
