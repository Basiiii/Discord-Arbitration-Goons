"""
Copyright © Basi

Github: https://github.com/basiiii
Website: https://basi.is-a.dev/
Discord: basi__

🏛️ Private discord bot for Warframe Arbitrations made with Discord.py.
https://discord.gg/arbitrations
"""

from discord.ext import commands
from discord.ext.commands import Context
import discord
from discord.ui import Select, View
from discord.ext import commands

from helpers import checks

class MySelect(View):

  @discord.ui.select(
    placeholder="Select section here.",
    options=[
      discord.SelectOption(label="General", value="1", description="General commands.", emoji="<:arbigoons:1100496365412438087>"),
    ]
  )

  async def select_callback(self, interaction, select):
    select.disabled=True
    if select.values[0] == "1":
      embed = discord.Embed(
            title="General.",
            color=0xf02023,
            description=
            """
            :ping_pong: ``..ping`` - ping the bot through API.
            <:PepeBusiness:1100436809877573712> ``..link`` - get the Arbi discord link.
            <:nerdge:1100436793708515438> ``..arbi`` - get the current arbitration.
            """
        )
      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1100368241005699132/1100489963809812511/ArbiLogo.png")
      await interaction.response.edit_message(embed=embed)

class Help(commands.Cog, name="help", description="Arbi's help menu."):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
      name="help",
      description="Navigate through help."
    )
    async def help(self, context: Context) -> None:
      """
        Use this command to view Arbi's help menu.
      """
      view = MySelect()
      embed = discord.Embed(
        title="Arbitration Goons help.",
            color=0xf02023,
      )
      embed.add_field(name="Arbitration bot commands support.",
      value="""
      Navigate through our commands using the menu button underneath.
      Click the field and select the type of commands you need help with.
      """,
      inline=False)
      embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1100368241005699132/1100489963809812511/ArbiLogo.png"
      )
      await context.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))
