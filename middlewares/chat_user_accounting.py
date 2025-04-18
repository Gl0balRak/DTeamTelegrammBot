from email.policy import default

from aiogram.types.update import Update
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import (TelegramObject)

from typing import Dict, Set


chats_users: Dict[int, Set[int]] = dict()


class UserAccounting(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Update):
            message: Message = event.message
            if message.from_user.id not in chats_users.setdefault(message.chat.id, set()):
                chats_users[message.chat.id].add(message.from_user.id)

        return await handler(event, data)

