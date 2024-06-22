from typing import Final
import os
import discord

TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
TEST_GUILD: Final[str] = discord.Object(id=int(os.getenv("TEST_GUILD")))
DATABASE_URL: Final[str] = (
    f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@db/{os.getenv("POSTGRES_DB")}"
)
