import logging
from discord import Interaction, Member, app_commands
from discord.ext import commands
from bot import DiscordBot
from constants import TEST_GUILD


class DevelopmentCommands(commands.Cog):
    def __init__(self, bot: DiscordBot):
        self.bot: DiscordBot = bot
        self.logger: logging.Logger = logging.getLogger("discord")
        self.show_join_date_ctx_menu = app_commands.ContextMenu(
            name="Show join date", callback=self.get_joined_date
        )
        self.maybe_ban_user_ctx_menu = app_commands.ContextMenu(
            name="Maybe ban user", callback=self.ban_user
        )

        self._add_ctx_menus()

    def _add_ctx_menus(self):
        self.bot.tree.add_command(self.show_join_date_ctx_menu)
        self.bot.tree.add_command(self.maybe_ban_user_ctx_menu)

    @app_commands.command()
    async def speak(self, ctx: Interaction):
        await ctx.response.send_message("I speak!")

    @app_commands.command()
    async def react(self, ctx: Interaction):
        await ctx.response.send_message("Very cool message!", ephemeral=True)

    @app_commands.command(
        name="sync_commands",
        description="Synchronizes commands, context menu options, etc. with the test guild.",
    )
    async def sync_commands(self, ctx: Interaction):
        """
        Use this after creating new command or context menu option,
        to immediately sync and make it work in TEST_GUILD.
        """
        self.logger.info("Syncing commands with the test guild.")

        # self.bot.tree.clear_commands(guild=TEST_GUILD)

        self.bot.tree.copy_global_to(guild=TEST_GUILD)
        synced_commands = await self.bot.tree.sync(guild=TEST_GUILD)

        await ctx.response.send_message(
            f"Commands synchronised: {[str(cmd) for cmd in synced_commands]}",
            ephemeral=True,
        )

    @app_commands.command(
        name="sync_commands_global",
        description="Synchronizes commands, context menu options, etc. with all guild. "
        "May take about 1 hour. ",
    )
    async def sync_commands_global(self, interation: Interaction):
        """
        Use this after creating new command or context menu option
        to sync them with all servers. This may take up to about 1 hour, before
        actions appear (dissapear) in the end servers.
        """
        self.logger.info(
            "Synchronizing commands with all bot discord servers, this may take about 1 hour to see in the end discord servers."
        )
        commands = await self.bot.tree.sync()
        await interation.response.send_message(
            f"Commands synchronised: {[f'{command}\n' for command in commands]}",
            ephemeral=True,
        )

    @app_commands.command(
        name="copy_cmds_to_test_guild",
        description="Copies commands to the test guild.",
    )
    async def copy_commands_global(self, ctx: Interaction):
        self.logger.info("Copying commands to the test guild.")
        self.bot.tree.copy_global_to(guild=TEST_GUILD)
        await ctx.response.send_message(
            "Copied commands to the test guild.", ephemeral=True
        )

    async def get_joined_date(self, interaction: Interaction, member: Member):
        await interaction.response.send_message(
            f"Member joined: {member.joined_at} ", ephemeral=True
        )

    async def ban_user(self, interaction: Interaction, member: Member):
        await interaction.response.send_message(
            f"Should I actually ban {member}...", ephemeral=True
        )


async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(DevelopmentCommands(bot))
