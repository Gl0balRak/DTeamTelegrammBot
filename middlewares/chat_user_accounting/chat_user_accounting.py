from aiogram.types.update import Update
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import (TelegramObject)

from typing import Dict, Set

import os

from middlewares.chat_user_accounting import CHAT_USER_ACCOUNTING_FILE

from itertools import islice

chats_users: Dict[int, Set[int]] = dict()

def init_chat_user_accounting():
    global chats_users

    if os.path.exists(CHAT_USER_ACCOUNTING_FILE):
        # Load data from file
        chats_users = dict()

        with open(CHAT_USER_ACCOUNTING_FILE, "r") as f:
            for line in islice(f, 1, None):
                chat_id, user_id = map(int, line.split(','))

                if chat_id in chats_users.keys():
                    chats_users[chat_id].add(user_id)
                else:
                    chats_users.update({chat_id: {user_id}})
        return

    # Create empty file
    with open(CHAT_USER_ACCOUNTING_FILE, "w") as f:
        f.write("ChatID,Username\n")

def add_new_chat_user(chat_id: int, user_id: str) -> None:
    with open(CHAT_USER_ACCOUNTING_FILE, "a") as f:
        f.write(f"{chat_id},{user_id}\n")


class ChatUserAccounting(BaseMiddleware):
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
                add_new_chat_user(message.chat.id, message.from_user.id)

        return await handler(event, data)
