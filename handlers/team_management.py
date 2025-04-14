from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


team_management_router = Router()

@team_management_router.message(Command("all"))
async def cmd_start(message: Message):
    chat_members = await message.bot.get_chat(message.chat.id)
    print(chat_members.active_usernames)
    print(chat_members)
    print("diche")
    await message.answer('Охайо, православные')