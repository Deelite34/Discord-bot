import logging
import discord
from discord.ext import commands
from sqlalchemy import func, select
from bot import DiscordBot
from models import Guild, Settings


class BaseBehaviour(commands.Cog):
    def __init__(self, bot: DiscordBot):
        self.bot: DiscordBot = bot
        self.logger: logging.Logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """create initial db data for newly joined server"""

        self.logger.info(f"Bot added to guild: {guild.name}")
        async with self.bot.db.create_session() as session:
            query = (
                select(func.count()).select_from(Guild).where(Guild.id == str(guild.id))
            )
            guild_in_db = await session.scalar(query)
            if not guild_in_db:
                db_guild = Guild(id=str(guild.id))
                guild_settings = Settings(id=db_guild.id)
                try:
                    session.add_all(instances=[db_guild, guild_settings])
                    await session.commit()
                    self.logger.info(
                        f"Created bot base db data in the server: {guild.name}"
                    )
                except Exception as e:
                    self.logger.warning(
                        f"Failed to create bot base db data for the server {guild.name} due to exception:"
                    )
                    raise e


async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(BaseBehaviour(bot))
