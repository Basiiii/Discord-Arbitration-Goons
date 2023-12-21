"""
Copyright © Basi

Github: https://github.com/basiiii
Website: https://basi.is-a.dev/
Discord: basi__

🏛️ Private discord bot for Warframe Arbitrations made with Discord.py.
https://discord.gg/arbitrations
"""

import json
import psutil
import os
import sys
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="killwarframe",
        description="Close the Warframe Program if opened",
    )
    @app_commands.describe(scope="Kill Warframe")
    @commands.check_any(commands.is_owner(), commands.has_role("Arbmin"))
    async def killwarframe(self, context: Context) -> None:
        for proc in psutil.process_iter(['pid', 'name']):
            if 'warframe' in proc.info['name'].lower():
                proc.terminate()
        embed = discord.Embed(
            title="Warframe closed",
            color=0xf02023
        )
        await context.send(embed=embed)

    @commands.command(
        name="restart",
        description="Restarts the bot.",
    )
    @app_commands.describe(scope="Restart bot.")
    @commands.check_any(commands.is_owner(), commands.has_role("Arbmin"))
    async def restart(self, context: Context) -> None:
        """
        Restarts the bot.
        """
        await context.send("Restarting bot...")
        os.execv(sys.executable, ['python'] + sys.argv)     
        
    @commands.command(
        name="read_json",
        description="Read the contents of a JSON file."
    )
    @commands.check_any(commands.is_owner(), commands.has_role("Arbmin"))
    async def read_json(self, context: commands.Context, file_path: str) -> None:
        """
        Read the contents of a JSON file.
        """
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            await context.send("The specified JSON file was not found.")
            return
        except json.JSONDecodeError:
            await context.send("Error decoding the JSON file.")
            return

        await context.send(f"Contents of JSON file `{file_path}`:\n```json\n{json.dumps(json_data, indent=4)}```")


    @commands.command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @checks.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                title="Slash Commands Sync",
                description="Slash commands have been globally synchronized.",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                title="Slash Commands Sync",
                description="Slash commands have been synchronized in this guild.",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Invalid Scope",
            description="The scope must be `global` or `guild`.",
            color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="Unsynchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global`, `current_guild` or `guild`")
    @checks.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Unsynchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global`, `current_guild` or `guild`.
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                title="Slash Commands Unsync",
                description="Slash commands have been globally unsynchronized.",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                title="Slash Commands Unsync",
                description="Slash commands have been unsynchronized in this guild.",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Invalid Scope",
            description="The scope must be `global` or `guild`.",
            color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    @app_commands.describe(cog="The name of the cog to load")
    @checks.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The bot will load the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not load the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Load",
            description=f"Successfully loaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @checks.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not unload the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Unload",
            description=f"Successfully unloaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @checks.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not reload the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Reload",
            description=f"Successfully reloaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @commands.check_any(commands.is_owner(), commands.has_role("Arbmin"))
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @checks.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @checks.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(
            description=message,
            color=0x9C84EF
        )
        await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Owner(bot))
