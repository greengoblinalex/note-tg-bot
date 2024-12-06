from aiogram.fsm.state import StatesGroup, State


class CreateOrUpdateNoteStates(StatesGroup):
    waiting_for_category = State()
    waiting_for_title = State()
    waiting_for_text = State()
