from decouple import config as env_config

# telegram
BOT_TOKEN = env_config("BOT_TOKEN")

# notes
NOTES_PER_PAGE = env_config("NOTES_PER_PAGE", default=5, cast=int)
FILTERS_PER_PAGE = env_config("FILTERS_PER_PAGE", default=4, cast=int)

# database
DATABASE_URL = env_config("DATABASE_URL", default="sqlite+aiosqlite:///data/db.sqlite3")
