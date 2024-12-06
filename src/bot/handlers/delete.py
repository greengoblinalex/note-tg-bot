from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.database import managers
from ..callback_datas import NoteCallbackData
from ..keyboards import main_menu_kb
from ..utils import get_page_by_note_id

router = Router()


@router.callback_query(NoteCallbackData.filter(F.action == "delete_note"))
async def delete_note(callback: CallbackQuery, callback_data: NoteCallbackData):
    page = await get_page_by_note_id(callback.from_user.id, callback_data.id)
    await managers.delete_note(callback_data.id)
    user = await managers.get_or_create_user(callback.from_user.id)

    notes_on_page = await managers.get_notes(callback.from_user.id, page)
    if not notes_on_page:
        page = max(0, page - 1)

    filtered_notes = (
        await managers.filter_notes_by_category(user.current_category)
        if user.current_category
        else None
    )
    await callback.message.edit_text(
        text="Выберите команду или заметку:",
        reply_markup=await main_menu_kb(
            callback.from_user.id, page=page, filtered_notes=filtered_notes
        ),
    )