from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from src.database import managers
from ..states import CreateOrUpdateNoteStates
from ..keyboards import main_menu_kb, note_kb, edit_kb
from ..callback_datas import NoteCallbackData

router = Router()


@router.callback_query(F.data == "create_note")
@router.callback_query(NoteCallbackData.filter(F.action == "update_note"))
async def create_or_update_note_start(callback: CallbackQuery, state: FSMContext):
    if ":" in callback.data and callback.data.split(":")[1] == "update_note":
        note = await managers.get_note_by_id(callback.data.split(":")[2])
        await state.update_data(note_id=note.id)
        await state.update_data(category=note.category)
        await state.update_data(title=note.title)
        await state.update_data(content=note.text)
        instruction_message = await callback.message.answer(
            "Введите новую категорию заметки:", reply_markup=edit_kb()
        )
    else:
        instruction_message = await callback.message.answer(
            "Введите категорию заметки:"
        )

    await state.update_data(instruction_message_id=instruction_message.message_id)
    await state.update_data(main_menu_message_id=callback.message.message_id)
    await state.set_state(CreateOrUpdateNoteStates.waiting_for_category)


@router.message(CreateOrUpdateNoteStates.waiting_for_category)
async def create_or_update_note_category(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.lower() != "пропустить":
        await state.update_data(category=message.text)
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=user_data["instruction_message_id"]
    )
    await message.delete()
    instruction_message = await message.answer(
        "Введите заголовок заметки:", reply_markup=edit_kb()
    )
    await state.update_data(instruction_message_id=instruction_message.message_id)
    await state.set_state(CreateOrUpdateNoteStates.waiting_for_title)


@router.message(CreateOrUpdateNoteStates.waiting_for_title)
async def create_or_update_note_title(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.lower() != "пропустить":
        await state.update_data(title=message.text)
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=user_data["instruction_message_id"]
    )
    await message.delete()
    instruction_message = await message.answer(
        "Введите содержимое заметки:", reply_markup=edit_kb()
    )
    await state.update_data(instruction_message_id=instruction_message.message_id)
    await state.set_state(CreateOrUpdateNoteStates.waiting_for_text)


@router.message(CreateOrUpdateNoteStates.waiting_for_text)
async def create_or_update_note_text(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.lower() != "пропустить":
        text = message.text
    else:
        text = user_data.get("content", "")
    category, title = user_data["category"], user_data["title"]

    if "note_id" in user_data:
        new_note = await managers.update_note(
            user_data["note_id"], category, title, text
        )
        try:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=user_data["main_menu_message_id"],
                text=(
                    f"Category: {new_note.category}\nTitle: {new_note.title}"
                    f"\nCreated at: {new_note.created_at.strftime('%d.%m.%y %H:%M')}\nUpdated at: {new_note.updated_at.strftime('%d.%m.%y %H:%M')}"
                    f"\n\n(Нажмите на текст заметки, чтобы скопировать его)\n<code>{new_note.text}</code>"
                ),
                reply_markup=await note_kb(new_note.id),
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                pass
    else:
        await managers.create_note(message.from_user.id, category, title, text)
        new_reply_markup = await main_menu_kb(message.from_user.id, 0)
        await message.bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=user_data["main_menu_message_id"],
            reply_markup=new_reply_markup,
        )

    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=user_data["instruction_message_id"]
    )
    await message.delete()

    await state.clear()
