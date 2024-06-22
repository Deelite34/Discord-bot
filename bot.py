import asyncio
import logging
import logging.handlers
from logger import setup_logger
from discord import Intents
from discord.ext import commands
from constants import DATABASE_URL, TOKEN
from db import DatabaseSingleton


logger = logging.getLogger("discord")
setup_logger(logger)

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.db = DatabaseSingleton(DATABASE_URL)
        super().__init__(*args, **kwargs)
        # Querying:  async with bot_instance_name.db.create_session() as session: ...

    async def setup_hook(self):
        await self.db.init_db()


bot: DiscordBot = DiscordBot(command_prefix="!", intents=intents)


async def main() -> None:
    async with bot:
        await bot.load_extension("cogs.dev")
        await bot.start(TOKEN)


if __name__ == "__main__":
    # bot.tree.sync()
    asyncio.run(main())
