from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.config import BOT_TOKEN
from .handlers import (
    start_router,
    create_or_update_note_router,
    view_note_router,
    pagination_router,
    filter_router,
    back_router,
    delete_router,
)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_router)
dp.include_router(create_or_update_note_router)
dp.include_router(view_note_router)
dp.include_router(pagination_router)
dp.include_router(filter_router)
dp.include_router(back_router)
dp.include_router(delete_router)


async def set_commands():
    commands = [BotCommand(command="start", description="Старт")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
