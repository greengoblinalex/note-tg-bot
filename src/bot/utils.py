from src.database.managers import get_notes
from src.config import NOTES_PER_PAGE


async def get_page_by_note_id(user_id: int, note_id: int) -> int:
    notes = await get_notes(user_id=user_id)
    index = next((i for i, note in enumerate(notes) if note.id == note_id), None)
    if index is not None:
        return index // NOTES_PER_PAGE
    return 0
