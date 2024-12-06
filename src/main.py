import asyncio

from src.database import create_tables
from src.bot import dp, bot, set_commands


async def main():
    await create_tables()
    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
