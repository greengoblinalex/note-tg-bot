from aiogram import Router, F
from aiogram.types import Message

from src.bot.keyboards import main_menu_kb
from src.database import managers

router = Router()


@router.message(F.text == "/start")
async def send_welcome(message: Message):
    user = await managers.get_or_create_user(message.from_user.id)
    user = await managers.get_or_update_user(user.tg_id, current_category=None)
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id
    )
    await message.answer(
        "Выберите команду или заметку:",
        reply_markup=await main_menu_kb(user.tg_id, 0),
    )
