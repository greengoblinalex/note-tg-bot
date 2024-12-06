from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import desc

from src.database.models import User, Note
from src.database import connection
from src.config import NOTES_PER_PAGE


@connection
async def get_or_create_user(session: AsyncSession, tg_id: int) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))

        if not user:
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            print(f"Зарегистрировал пользователя с ID {tg_id}!")
            return new_user

        await session.refresh(user)
        print(f"Пользователь с ID {tg_id} найден!")
        return user
    except SQLAlchemyError as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()
        return None


@connection
async def get_or_update_user(
    session: AsyncSession, tg_id: int, **kwargs
) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=tg_id))

        if not user:
            new_user = User(tg_id=tg_id, **kwargs)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            print(f"Зарегистрировал пользователя с ID {tg_id}!")
            return new_user

        for key, value in kwargs.items():
            setattr(user, key, value)

        await session.commit()
        await session.refresh(user)
        print(f"Пользователь с ID {tg_id} обновлен!")
        return user
    except SQLAlchemyError as e:
        print(f"Ошибка при обновлении пользователя: {e}")
        await session.rollback()
        return None


@connection
async def create_note(
    session: AsyncSession, user_id: int, category: str, title: str, text: str
) -> Optional[Note]:
    try:
        user = await session.scalar(select(User).filter_by(tg_id=user_id))
        if not user:
            print(f"Пользователь с ID {user_id} не найден.")
            return None

        new_note = Note(
            user_id=user_id,
            category=category.strip().title(),
            title=title.strip().title(),
            text=text.strip(),
        )

        session.add(new_note)
        await session.commit()
        await session.refresh(new_note)
        print(f"Заметка для пользователя с ID {user_id} успешно добавлена!")
        return new_note
    except SQLAlchemyError as e:
        print(f"Ошибка при добавлении заметки: {e}")
        await session.rollback()
        return None


@connection
async def update_note(
    session: AsyncSession,
    note_id: int,
    category: Optional[str] = None,
    title: Optional[str] = None,
    text: Optional[str] = None,
) -> Optional[Note]:
    try:
        note = await session.scalar(select(Note).filter_by(id=note_id))

        if not note:
            print(f"Заметка с ID {note_id} не найдена.")
            return None

        if category:
            note.category = category.strip().title()

        if title:
            note.title = title.strip().title()

        if text:
            note.text = text.strip()

        await session.commit()
        await session.refresh(note)
        print(f"Заметка с ID {note_id} успешно отредактирована!")
        return note
    except SQLAlchemyError as e:
        print(f"Ошибка при редактировании заметки: {e}")
        await session.rollback()
        return None


@connection
async def delete_note(session: AsyncSession, note_id: int) -> bool:
    try:
        note = await session.scalar(select(Note).filter_by(id=note_id))

        if not note:
            print(f"Заметка с ID {note_id} не найдена.")
            return False

        await session.delete(note)
        await session.commit()
        print(f"Заметка с ID {note_id} успешно удалена!")
        return True
    except SQLAlchemyError as e:
        print(f"Ошибка при удалении заметки: {e}")
        await session.rollback()
        return False


@connection
async def filter_notes_by_category(
    session: AsyncSession, search_text: str
) -> list[Note]:
    try:
        if search_text == "All":
            result = await session.execute(select(Note).order_by(desc(Note.created_at)))
        else:
            result = await session.execute(
                select(Note)
                .filter(Note.category == search_text)
                .order_by(desc(Note.created_at))
            )
        notes = result.scalars().all()
        return notes
    except SQLAlchemyError as e:
        print(f"Ошибка при поиске заметок: {e}")
        return []


@connection
async def get_notes(
    session: AsyncSession, user_id: int, page: int = None
) -> list[Note]:
    try:
        query = select(Note).filter_by(user_id=user_id).order_by(desc(Note.created_at))
        if page is not None:
            query = query.offset(page * NOTES_PER_PAGE).limit(NOTES_PER_PAGE)

        result = await session.execute(query)
        notes = result.scalars().all()
        return notes
    except SQLAlchemyError as e:
        print(f"Ошибка при получении заметок: {e}")
        return []


@connection
async def get_note_by_id(session: AsyncSession, note_id: int) -> Optional[Note]:
    try:
        note = await session.scalar(select(Note).filter_by(id=note_id))
        return note
    except SQLAlchemyError as e:
        print(f"Ошибка при получении заметки: {e}")
        return None
