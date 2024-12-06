from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.database import managers
from ..keyboards import main_menu_kb, categories_kb
from ..callback_datas import CategoryCallbackData

router = Router()


@router.callback_query(F.data == "filter_notes")
async def start_filter_notes(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите категорию для фильтрации заметок:",
        reply_markup=await categories_kb(callback.from_user.id),
    )


@router.callback_query(CategoryCallbackData.filter(F.action == "next_page"))
async def next_page(callback: CallbackQuery, callback_data: CategoryCallbackData):
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await categories_kb(callback.from_user.id, callback_data.page),
    )


@router.callback_query(CategoryCallbackData.filter(F.action == "prev_page"))
async def prev_page(callback: CallbackQuery, callback_data: CategoryCallbackData):
    await callback.message.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await categories_kb(callback.from_user.id, callback_data.page),
    )


@router.callback_query(CategoryCallbackData.filter(F.action == "select_category"))
async def filtered_notes(callback: CallbackQuery, callback_data: CategoryCallbackData):
    filtered_notes = await managers.filter_notes_by_category(callback_data.name)
    await managers.get_or_update_user(
        callback.from_user.id, current_category=callback_data.name
    )
    await callback.message.edit_text(
        text="Выберите команду или заметку:",
        reply_markup=await main_menu_kb(
            callback.message.from_user.id, filtered_notes=filtered_notes
        ),
    )
