from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config import NOTES_PER_PAGE, FILTERS_PER_PAGE
from src.database.managers import get_notes
from .callback_datas import NoteCallbackData, CategoryCallbackData


async def main_menu_kb(user_id, page=0, filtered_notes=None):
    keyboard = InlineKeyboardBuilder()

    if not filtered_notes:
        notes = await get_notes(user_id=user_id, page=page)
        total_notes = await get_notes(user_id=user_id)
    else:
        notes = filtered_notes[page * NOTES_PER_PAGE : (page + 1) * NOTES_PER_PAGE]
        total_notes = filtered_notes

    for i in range(0, len(notes), 1):
        row_buttons = [
            InlineKeyboardButton(
                text=note.title,
                callback_data=NoteCallbackData(action="view", id=note.id).pack(),
            )
            for note in notes[i : i + 1]
        ]
        keyboard.row(*row_buttons)

    keyboard.row(
        InlineKeyboardButton(text="Add Note", callback_data="create_note"),
        InlineKeyboardButton(text="Filter Notes", callback_data="filter_notes"),
    )

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="<",
                callback_data=NoteCallbackData(
                    action="prev_page", page=page - 1
                ).pack(),
            )
        )
    if (page + 1) * NOTES_PER_PAGE < len(total_notes):
        navigation_buttons.append(
            InlineKeyboardButton(
                text=">",
                callback_data=NoteCallbackData(
                    action="next_page", page=page + 1
                ).pack(),
            )
        )

    if navigation_buttons:
        keyboard.row(*navigation_buttons)

    return keyboard.as_markup()


async def categories_kb(user_id, page=0):
    keyboard = InlineKeyboardBuilder()

    notes = await get_notes(user_id=user_id)
    categories = list(set([note.category for note in notes]))

    keyboard.row(
        InlineKeyboardButton(
            text="All",
            callback_data=CategoryCallbackData(
                action="select_category", name="All"
            ).pack(),
        )
    )

    start_index = page * FILTERS_PER_PAGE
    end_index = start_index + FILTERS_PER_PAGE
    paginated_categories = categories[start_index:end_index]

    for category in paginated_categories:
        keyboard.row(
            InlineKeyboardButton(
                text=category,
                callback_data=CategoryCallbackData(
                    action="select_category", name=category
                ).pack(),
            )
        )

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="<",
                callback_data=CategoryCallbackData(
                    action="prev_page", page=page - 1
                ).pack(),
            )
        )
    if end_index < len(categories):
        navigation_buttons.append(
            InlineKeyboardButton(
                text=">",
                callback_data=CategoryCallbackData(
                    action="next_page", page=page + 1
                ).pack(),
            )
        )

    if navigation_buttons:
        keyboard.row(*navigation_buttons)

    return keyboard.as_markup()


async def note_kb(note_id):
    keyboard = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(
                    text="Edit",
                    callback_data=NoteCallbackData(
                        action="update_note", id=note_id
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Delete",
                    callback_data=NoteCallbackData(
                        action="delete_note", id=note_id
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data=NoteCallbackData(action="back", id=note_id).pack(),
                ),
            ],
        ]
    )

    return keyboard.as_markup()
