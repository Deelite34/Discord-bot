import asyncio
import logging
import logging.handlers
import os
from logger import setup_logger
from discord import Intents
from discord.ext import commands
from constants import DATABASE_URL, TEST_GUILD, TOKEN
from db import DatabaseSingleton


logger = logging.getLogger("discord")
setup_logger(logger)


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.db = DatabaseSingleton(DATABASE_URL)
        self.logger = logger
        super().__init__(*args, **kwargs)

    async def load_cogs(self):
        for file in os.listdir(os.path.dirname(__file__) + "/cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                await bot.load_extension(f"cogs.{name}")
                self.logger.info(f"Loaded cog: {name}")

    async def setup_hook(self):
        await self.db.init_db()
        await self.load_cogs()
        self.logger.info(f"Using guild id {TEST_GUILD.id}")
        self.logger.info(f"Bot {self.user} has logged in!")


intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
bot: DiscordBot = DiscordBot(command_prefix="!", intents=intents)


async def main() -> None:
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

    # After bot is shut down or crashes
    bot.db.close_async()
