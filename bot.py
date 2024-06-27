import asyncio
import logging
import logging.handlers
from logger import setup_logger
from discord import Intents
from discord.ext import commands
from constants import DATABASE_URL, TOKEN
from db import DatabaseSingleton


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.db = DatabaseSingleton(DATABASE_URL)
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        await self.db.init_db()


intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
bot: DiscordBot = DiscordBot(command_prefix="!", intents=intents)


async def main() -> None:
    logger = logging.getLogger("discord")
    setup_logger(logger)

    async with bot:
        await bot.load_extension("cogs.dev")
        await bot.load_extension("cogs.base")
        await bot.load_extension("cogs.gambling")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

    # After bot is shut down or crashes
    bot.db.close_async()
