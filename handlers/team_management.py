from email.policy import default

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ResultChatMemberUnion
from decouple import config

from typing import List

from middlewares.chat_user_accounting import chats_users

team_management_router = Router()


async def get_chat_members_mention(message, delimiter=", "):
    chat_members: List[ResultChatMemberUnion] = [
        await c for c in [
            message.bot.get_chat_member(message.chat.id, user_id)
            for user_id in chats_users.setdefault(message.chat.id, [])
        ]
    ]

    return delimiter.join([f'@{member.user.username}' for member in chat_members])

@team_management_router.message(Command("all"))
async def cmd_start(message: Message):
    if response := await get_chat_members_mention(message):
        await message.answer(response)


@team_management_router.message(Command("task"))
async def cmd_start(message: Message):
    chat_admins = map(lambda x: x.user.id, await message.bot.get_chat_administrators(message.chat.id))

    response: str = ""
    if message.from_user.id in chat_admins:
        response += await get_chat_members_mention(message) + "\n"

    await message.answer(response + f"{config('TASK_BOARD_LINK')}")

