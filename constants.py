from typing import Final
import os
import discord

TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
TEST_GUILD: Final[str] = discord.Object(id=int(os.getenv("TEST_GUILD")))
DB_USERNAME = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL: Final[str] = (
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@db/{DB_NAME}"
)
