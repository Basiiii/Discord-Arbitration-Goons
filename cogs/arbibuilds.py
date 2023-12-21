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

class Builds(commands.Cog, name="Builds", description="Arbitration builds database."):
    def __init__(self, bot):
        self.bot = bot

#     @commands.hybrid_command(
#       name="builds",
#       description="Navigate through builds database."
#     )
#     async def builds(self, context: Context) -> None:
#       """
#         Use this command to view Arbitration builds.
#       """
#       builds = Select(
#         placeholder="Select build here.",
#         options=[
#           discord.SelectOption(label="Saryn", value="1", emoji="<:arbigoons:1100496365412438087>"),
#           discord.SelectOption(label="Wisp", value="2", emoji="<:arbigoons:1100496365412438087>"),
#           discord.SelectOption(label="Volt", value="3", emoji="<:arbigoons:1100496365412438087>"),
#           discord.SelectOption(label="Mirage", value="4", emoji="<:arbigoons:1100496365412438087>")
#         ]
#       )

#       async def builds_callback(interaction):
#         if builds.values[0] == "1":
#           embed = discord.Embed(
#                 title="Saryn Arbi build.",
#                 color=0xff0000,
#                 description=
#                 """
#                 🔻Saryn is the primary DPS - **Don’t take this role for defense if you’re newer to arbi.**

#                 - Toxic lash applies 138% of weapons total damage as toxin alongside all sources of damage (not combining) including nightwatch napalm's fire ticks and contagion's toxin cloud ticks. This triple dips bane/roar. Lash benefits from venom, thermal, shock trooper, smite, vex, amp  etc.

#                 - Venom dose will give the team additional corrosive base damage, which will increase the scaling with roar and eclipse multiplicative damage buffs for initial damage.

#                 - Contagion cloud also allows saryn to see damage ticks on screen from the toxin clouds as soon as mobs spawn to allow for easy spotting and faster kill times. Which is important since only 5 arbi drones can be spawned in at one given time. Clouds are 10m wide and last 20 seconds per enemy killed while toxic lash is up.
#                 To reduce strain on GPU go settings > accessibility > visual effects intensity: (type it in) 0/200.

#                 Xata’s Whisper doesn’t currently have an augment, and only self buffs. Provides 120% of your total weapon damage as void damage to all instances similar to toxic lash. Xata’s for carry pants dps 90-100w defense enemy scaling 1400+, Nourish for Interception.
#                 Nourish subsume doesn't require an augment and provides 693% modded viral damage to allies for 37 seconds. It has a 25m radius and persists.
#                 Energized Munitions can be used for comfort or if you prefer to constantly spam fire.

#                 *Madurai focus tree with phoenix talons for an additional 30% physical damage passive and void strike active with fuel’s 40% ammo efficiency. Run vazarin dash instead if running with inexperienced supports in order to safeguard operative for emergencies. 
                
#                 More information available in arbitration document.
#                 https://docs.google.com/document/d/14yAA4rv82MVjDJKasm70oL_peegCHPQioDeMGdvf4DM/edit
#                 """
#             )
#           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/937368742462124042/1019362449977262120/arbi.png")
#           embed.set_image(url="https://cdn.discordapp.com/attachments/1038479128480993424/1095705677575499947/image.png")
#           embed.set_footer(
#             text="Build from Arbi doc.",
#             icon_url="https://cdn.discordapp.com/attachments/1100368241005699132/1100489963809812511/ArbiLogo.png"
#           )
#           await interaction.response.edit_message(embed=embed)
        
#         if builds.values[0] == "2":
#           embed = discord.Embed(
#                 title="Wisp Arbi build.",
#                 color=0xff0000,
#                 description=
#                 """
#                 🔻Wisp's primary focus is to provide buffs, but you still help with kills via sporelancer

#                 - Shock mote isn't necessary if trying to cover 3 separate camp spots. Other than that it’s good to throw down as it provides a meaningful form of cc that will end up covering a lot of area due to specters and kavats picking up shock mote as well.

#                 - Be sure to spawn a Nidus specter and wait for tether before placing motes in key positions, as they will keep that 1.51x final strength multiplier for the rest of the arbitration.

#                 Roar subsume ☆ is the primary build, providing a 25m radius multiplicative damage boost for the team. Try to land buff on all teammates if you can, but focus on saryn.
#                 Banish subsume can be run if going past 100 waves to ensure safety of the defense operative, they're stupid and will follow a random player at any given point while they collect vitus essence. Banish lasts 32 seconds, teammates hit by it can just roll out of banishment if they get affected.

#                 *Take Madurai for the 40% strength on double void sling, pairs well with at least one teammate running Zenurik’s 20% from hardened wellspring and Molt Augmented 60% You will have to replace your motes after reaching molt aug 250 stacks, then spawn protea specter.
                
#                 More information available in arbitration document.
#                 https://docs.google.com/document/d/14yAA4rv82MVjDJKasm70oL_peegCHPQioDeMGdvf4DM/edit
#                 """
#             )
#           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/937368742462124042/1019362449977262120/arbi.png")
#           embed.set_image(url="https://cdn.discordapp.com/attachments/1038479128480993424/1095706130124111932/image.png")
#           embed.set_footer(
#             text="Build from Arbi doc.",
#             icon_url="https://cdn.discordapp.com/attachments/1100368241005699132/1100489963809812511/ArbiLogo.png"
#           )
#           await interaction.response.edit_message(embed=embed)
        
#         if builds.values[0] == "3":
#           embed = discord.Embed(
#                 title="Volt Arbi build.",
#                 color=0xff0000,
#                 description=
#                 """
#                 🔻Volt is an alternative to chroma in terms of reload speed and damage buffs.

#                 - He feels nicer to use due to the high base range on his team reload buff and not having to worry about keeping vex armor stacked.

#                 - He increases ally movement speed to make collecting vitus essence faster so they can get back to covering spawns faster.

#                 - 95% reload speed buff with Molt Aug stacks and is re-castable at any point, it lasts 35 seconds with Molt Eff in a 20m radius, persists, and provides a 6.7x speed multiplier.

#                 - Shock trooper provides 383% electric to teams base damage, it lasts 116 seconds.

#                 - Volts electric shield can be used to grant further electric damage to shots fired through it as well as doubling critical damage. This lasts 73 seconds. Can be used strategically for operative.

#                 Thermal sunder ☆ subsume adds 287% heat and 287% cold damage to teams’ base damage similar to Shock trooper, this lasts 130 seconds total, but does require the Thermal transfer augment mod. It leaves a zone for 43 seconds in a 10m radius, the buff constantly refreshes itself while inside the zone, it lasts 87 seconds after allies leave the zone.
#                 Energized Munitions can be used for comfort or if you prefer to constantly spam fire.

#                 *Set energy colors on frame to smoke black to help with visibility while Thermal transfer's zone is active.

#                 More information available in arbitration document.
#                 https://docs.google.com/document/d/14yAA4rv82MVjDJKasm70oL_peegCHPQioDeMGdvf4DM/edit
#                 """
#             )
#           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/937368742462124042/1019362449977262120/arbi.png")
#           embed.set_image(url="https://cdn.discordapp.com/attachments/1038479128480993424/1095706297204224103/image.png")
#           embed.set_footer(
#             text="Build from Arbi doc.",
#             icon_url="https://cdn.discordapp.com/attachments/1100368241005699132/1100489963809812511/ArbiLogo.png"
#           )
#           await interaction.response.edit_message(embed=embed)
        
#         if builds.values[0] == "4":
#           embed = discord.Embed(
#                 title="Mirage Arbi build.",
#                 color=0xff0000,
#                 description=
#                 """
#                 🔻Mirage is one of the key warframes in an arbi squad.

#                 - Eclipse provides a 924% final multiplicative buff to team damage. Buff does not persist when allies leave the area. 1,396% with nidus tether and 3 power dono and molt aug stacked.

#                 - When certain abilities are subsumed onto another frame they become slightly weaker, hence it is best to have a mirage in the squad. To ensure you're getting the most benefit from eclipse, go to graphic settings > graphics engine: enhanced > dynamic lighting: off > volumetric lighting: off . This will grant you higher damage % from eclipse no matter the light level.

#                 Dispensary ☆ when the player is below 70% energy/health or 70% ammo on primary or secondary (reserves). Lasts 20.5 seconds with 108% chance of double drop with max molt aug stacks, 2 other power dono on team and molt efficiency active.
#                 Nourish subsume doesn't require an augment and provides 618% viral damage to allies for 41 seconds. It has a 36m radius and persists. Highly effective for saryn’s lash.
#                 Elemental ward provides a 91% reload speed buff to the team within a 10m radius lasting 65 seconds. Toxin energy color on your frame. Ward can be used alongside volt, but does not stack with chroma’s. Can be used with Everlasting Ward augment and Narrow Minded (reload% scales off duration) instead of augur secrets and Energy conversion.

#                 More information available in arbitration document.
#                 https://docs.google.com/document/d/14yAA4rv82MVjDJKasm70oL_peegCHPQioDeMGdvf4DM/edit
#                 """
#             )
#           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/937368742462124042/1019362449977262120/arbi.png")
#           embed.set_image(url="https://cdn.discordapp.com/attachments/1038479128480993424/1095706575777320980/image.png")
#           embed.set_footer(
#             text="Build from Arbi doc.",
#             icon_url="https://cdn.discordapp.com/attachments/1100368241005699132/1100489963809812511/ArbiLogo.png"
#           )
#           await interaction.response.edit_message(embed=embed)
      
#       builds.callback = builds_callback

#       view = View()
#       view.add_item(builds)

#       embed = discord.Embed(
#         title="Arbitration builds database.",
#             color=0xff0000,
#       )
#       embed.add_field(name="How to use.",
#                       value=
#                       """
#                       To navigate through our builds please use the menus underneath. Simply choose a build from a category you would like to see and the bot will automatically display it.
#                       """,
#                       inline=False)
#       embed.set_thumbnail(
#         url="https://cdn.discordapp.com/attachments/937368742462124042/1019362449977262120/arbi.png"
#       )

#       await context.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Builds(bot))
