"""
Copyright © Basi

Github: https://github.com/basiiii
Website: https://basi.is-a.dev/
Discord: basi__

🏛️ Private discord bot for Warframe Arbitrations made with Discord.py.
https://discord.gg/arbitrations
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context

class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xf02023
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="link",
        description="Get the discord server link."
    )
    @commands.cooldown(2, 10, commands.BucketType.channel)
    async def link(self, context: Context) -> None:
        """
        Arbi goons discord link.
        """
        await context.send("https://discord.gg/arbitrations")

async def setup(bot):
    await bot.add_cog(General(bot))
