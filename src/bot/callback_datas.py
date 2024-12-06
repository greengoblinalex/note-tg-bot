from typing import Optional

from aiogram.filters.callback_data import CallbackData


class NoteCallbackData(CallbackData, prefix="note"):
    action: str
    id: Optional[int] = None
    page: Optional[int] = None


class CategoryCallbackData(CallbackData, prefix="category"):
    action: str
    name: Optional[str] = None
    page: Optional[int] = None
