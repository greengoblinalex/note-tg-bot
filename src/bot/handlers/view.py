from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.database import managers
from ..callback_datas import NoteCallbackData
from ..keyboards import note_kb

router = Router()


@router.callback_query(NoteCallbackData.filter(F.action == "view"))
async def get_note(callback: CallbackQuery, callback_data: NoteCallbackData):
    note = await managers.get_note_by_id(callback_data.id)
    await callback.message.edit_text(
        text=(
            f"Category: {note.category}\nTitle: {note.title}"
            f"\nCreated at: {note.created_at.strftime('%d.%m.%y %H:%M')}\nUpdated at: {note.updated_at.strftime('%d.%m.%y %H:%M')}"
            f"\n\n(Нажмите на текст заметки, чтобы скопировать его)\n<code>{note.text}</code>"
        ),
        reply_markup=await note_kb(note.id),
        parse_mode="HTML",
    )
