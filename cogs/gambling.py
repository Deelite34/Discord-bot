import datetime
import logging
import random
import discord
from discord.ext import commands
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncResult
from bot import DiscordBot
from discord import Interaction, app_commands

from models import GambleData, Settings


class Gambling(commands.Cog):
    def __init__(self, bot: DiscordBot):
        self.bot: DiscordBot = bot
        self.logger: logging.Logger = logging.getLogger("discord")

    @app_commands.command()
    async def gamble_status(self, ctx: Interaction):
        async with self.bot.db.create_session() as session:
            query = select(GambleData).where(GambleData.user_id == str(ctx.user.id))
            gamble_user = await session.scalar(query)
            await ctx.response.send_message(
                f"Current funds: {gamble_user.funds}\nlast gambled: {gamble_user.last_gamble}\nbankrupt until: {gamble_user.bankrupcy_cooldown_until or '-'}"
            )

    @app_commands.command()
    async def gamble_leaderboards(self, ctx: Interaction):
        async with self.bot.db.create_session() as session:
            query = select(GambleData).order_by(GambleData.funds.desc()).limit(10)
            top_gamblers = await session.execute(query)

            gamblers_txt = ""

            for index, gambler in enumerate(top_gamblers):
                gambler: GambleData
                member = ctx.guild.get_member(int(gambler[0].id))
                gamblers_txt = f"{gamblers_txt}**{index+1}. {member.display_name} - {gambler[0].funds}**\n"

            embed = discord.Embed(title="Richest gamblers")
            embed.add_field(name="", value=gamblers_txt, inline=False)

            await ctx.response.send_message(embed=embed)

    @app_commands.command(description="flat amount, % of funds, all or max")
    async def gamble(self, ctx: Interaction, gamble_amount: str):
        async with self.bot.db.create_session() as session:
            query = select(GambleData).where(GambleData.user_id == str(ctx.user.id))
            gamble_user = await session.scalar(query)

            query = select(
                Settings.gamble_starting_funds,
                Settings.gamble_bankrupt_cooldown,
                Settings.gamble_win_chance,
                Settings.id,
            ).where(Settings.id == str(ctx.guild.id))

            settings: AsyncResult = await session.execute(query)
            settings: AsyncResult = settings.first()

            if not gamble_user:
                gamble_user: GambleData = GambleData(
                    user_id=str(ctx.user.id),
                    guild=str(ctx.guild.id),
                    funds=settings.gamble_starting_funds,
                )
                session.add(gamble_user)
                await session.commit()
                query = (
                    select(GambleData)
                    .where(GambleData.user_id == str(ctx.user.id))
                    .with_for_update()
                )  # lock row just in case of race conditions
                gamble_user = await session.scalar(query)

            if gamble_user.bankrupcy_cooldown_until:
                if datetime.datetime.now() < gamble_user.bankrupcy_cooldown_until:
                    return await ctx.response.send_message(
                        f"You are bankrupt, wait until {gamble_user.bankrupcy_cooldown_until} to get new starting funds."
                    )
                else:
                    if gamble_user.funds <= 0:
                        gamble_user.bankrupcy_cooldown_until = None
                        gamble_user.funds = settings.gamble_starting_funds
            else:
                if gamble_user.funds <= 0:
                    gamble_user.bankrupcy_cooldown_until = None
                    gamble_user.funds = settings.gamble_starting_funds

            amount = None

            if gamble_amount == "all" or gamble_amount == "max":
                amount = gamble_user.funds
            elif "%" in gamble_amount:
                percentage = gamble_amount.split("%")[0]
                percentage = int(percentage) * 0.01
                amount = int(gamble_user.funds * percentage)
            else:
                amount = int(gamble_amount)

            if gamble_user.funds >= amount:
                user_has_won = (100 * random.random()) < settings.gamble_win_chance

                if user_has_won:
                    gamble_user.funds += amount
                    await ctx.response.send_message(f"You won {amount} credits!")
                else:
                    loss_msg = f"You lost {amount} credits!"
                    gamble_user.funds -= amount

                    if gamble_user.funds <= 0:
                        if settings.gamble_bankrupt_cooldown is not None:
                            gamble_user.bankrupcy_cooldown_until = (
                                datetime.datetime.now().replace(microsecond=0)
                                + datetime.timedelta(
                                    seconds=settings.gamble_bankrupt_cooldown
                                )
                            )

                            await ctx.response.send_message(
                                loss_msg
                                + f" \nYou lost all your credits. You need to wait until {gamble_user.bankrupcy_cooldown_until} to get new starting funds."
                            )
                        else:
                            await ctx.response.send_message(
                                loss_msg
                                + " \nHowever, because cooldown for bankrupts is not set, you can play again immidiately with new starting funds!"
                            )
                    else:
                        await ctx.response.send_message(loss_msg)

                gamble_user.last_gamble = datetime.datetime.now()
                await session.commit()
            else:
                await ctx.response.send_message("Not enough funds!")


async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(Gambling(bot))
