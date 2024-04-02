from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class CheckUserSubscription(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # SOME ACTIONS TO GET USER`s SUBSCRIPTION
        is_can_have_audio: bool = True
        is_user_have_sub: bool = True
        
        data['can_have_audio'] = is_can_have_audio
        data['user_subscribed'] = is_user_have_sub

        return await handler(event, data)
