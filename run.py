import asyncio

from create_bot import bot, dp

from handlers.start import start_router
from handlers.team_management import team_management_router

from middlewares.chat_user_accounting import UserAccounting


async def main():
    dp.include_router(start_router)
    dp.include_router(team_management_router)

    dp.update.outer_middleware(UserAccounting())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
