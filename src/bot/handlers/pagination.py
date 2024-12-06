from aiogram import Router, F
from aiogram.types import CallbackQuery

from ..callback_datas import NoteCallbackData
from ..keyboards import main_menu_kb

router = Router()


@router.callback_query(NoteCallbackData.filter(F.action == "next_page"))
async def next_page(callback: CallbackQuery, callback_data: NoteCallbackData):
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await main_menu_kb(callback.from_user.id, callback_data.page),
    )


@router.callback_query(NoteCallbackData.filter(F.action == "prev_page"))
async def prev_page(callback: CallbackQuery, callback_data: NoteCallbackData):
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await main_menu_kb(callback.from_user.id, callback_data.page),
    )
