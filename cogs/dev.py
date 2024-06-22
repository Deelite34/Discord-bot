import logging
from discord import Interaction, Member, Message, app_commands
from discord.ext import commands
from constants import TEST_GUILD
from responses import get_response


logger = logging.getLogger("discord")


class DevelopmentCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
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

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f"Using guild id {TEST_GUILD.id}")
        logger.info(f"Bot {self.bot.user} has logged in!")

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
        logger.info("Syncing commands with the test guild.")

        # self.bot.tree.copy_global_to(guild=TEST_GUILD)
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
        logger.info(
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
        logger.info("Copying commands to the test guild.")
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

    async def send_message(self, message: Message, user_message: str) -> None:
        """
        handles sending response to a command.
        User who preppends with question mark will receive response as direct message.
        """

        if not user_message:
            logger.info(
                "(Message was empty because intents were probably not enabled )"
            )
            return

        if send_priv_response := user_message[0] == "?":
            user_message = user_message[1:]

        try:
            response: str = get_response(user_message)
            if send_priv_response:
                await message.author.send(response)
            else:
                await message.channel.send(response)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        username: str = str(message.author)
        user_message: str = str(message.content)
        channel: str = str(message.channel)

        logger.info(f"[{channel}] {username}: '{user_message}'")
        await self.send_message(message, user_message)


async def setup(bot):
    await bot.add_cog(DevelopmentCommands(bot))
