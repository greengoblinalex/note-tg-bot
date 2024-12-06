import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.database import models
from src.database.managers import (
    get_or_create_user,
    get_or_update_user,
    create_note,
    update_note,
    delete_note,
    filter_notes_by_category,
    get_notes,
    get_note_by_id,
)

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, future=True)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def async_session():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    async with async_session_factory() as session:
        yield session


@pytest.mark.asyncio
async def test_get_or_create_user(async_session):
    user = await get_or_create_user(session=async_session, tg_id=12345)
    assert user is not None
    assert user.tg_id == 12345


@pytest.mark.asyncio
async def test_get_or_update_user(async_session):
    user = await get_or_update_user(tg_id=12345, session=async_session)
    assert user is not None
    assert user.tg_id == 12345


@pytest.mark.asyncio
async def test_create_note(async_session):
    user = await get_or_create_user(session=async_session, tg_id=12345)
    note = await create_note(
        user_id=user.tg_id,
        category="Test",
        title="Test Note",
        text="This is a test note.",
        session=async_session,
    )
    assert note is not None
    assert note.user_id == user.tg_id
    assert note.category == "Test"
    assert note.title == "Test Note"
    assert note.text == "This is a test note."


@pytest.mark.asyncio
async def test_update_note(async_session):
    user = await get_or_create_user(session=async_session, tg_id=12345)
    note = await create_note(
        user_id=user.tg_id,
        category="Test",
        title="Test Note",
        text="This is a test note.",
        session=async_session,
    )
    updated_note = await update_note(
        note_id=note.id,
        category="Updated",
        title="Updated Note",
        text="This is an updated test note.",
        session=async_session,
    )
    assert updated_note is not None
    assert updated_note.category == "Updated"
    assert updated_note.title == "Updated Note"
    assert updated_note.text == "This is an updated test note."


@pytest.mark.asyncio
async def test_delete_note(async_session):
    user = await get_or_create_user(session=async_session, tg_id=12345)
    note = await create_note(
        user_id=user.tg_id,
        category="Test",
        title="Test Note",
        text="This is a test note.",
        session=async_session,
    )
    result = await delete_note(note_id=note.id, session=async_session)
    assert result is True


@pytest.mark.asyncio
async def test_filter_notes_by_category(async_session):
    user = await get_or_create_user(session=async_session, tg_id=12345)
    await create_note(
        user_id=user.tg_id,
        category="Test",
        title="Test Note",
        text="This is a test note.",
        session=async_session,
    )
    notes = await filter_notes_by_category(search_text="Test", session=async_session)
    assert len(notes) > 0


@pytest.mark.asyncio
async def test_get_notes(async_session):
    user = await get_or_create_user(session=async_session, tg_id=12345)
    await create_note(
        user_id=user.tg_id,
        category="Test",
        title="Test Note",
        text="This is a test note.",
        session=async_session,
    )
    notes = await get_notes(user_id=user.tg_id, session=async_session)
    assert len(notes) > 0


@pytest.mark.asyncio
async def test_get_note_by_id(async_session):
    user = await get_or_create_user(session=async_session, tg_id=12345)
    note = await create_note(
        user_id=user.tg_id,
        category="Test",
        title="Test Note",
        text="This is a test note.",
        session=async_session,
    )
    fetched_note = await get_note_by_id(note_id=note.id, session=async_session)
    assert fetched_note is not None
    assert fetched_note.id == note.id
