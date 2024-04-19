from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.db.orm import get_user_have_sub


class CheckUserSubscription(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        is_user_have_sub: bool = await get_user_have_sub(data['session'], event.from_user.id)

        data['user_subscribed'] = is_user_have_sub

        return await handler(event, data)
