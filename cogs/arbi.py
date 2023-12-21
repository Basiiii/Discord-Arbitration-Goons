"""
Copyright © Basi

Github: https://github.com/basiiii
Website: https://basi.is-a.dev/
Discord: basi__

🏛️ Private discord bot for Warframe Arbitrations made with Discord.py.
https://discord.gg/arbitrations
"""

import json
from datetime import datetime, timedelta
import os
import sys
from dateutil.parser import isoparse
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import requests
from termcolor import colored, cprint

from helpers import checks
from helpers.utils import print_fatal, print_warning, print_info

"""
Check if 'config.json' exists, and exit if it doesn't.
Otherwise, load its contents into the 'config' variable.
"""
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(script_dir, "config.json")

if not os.path.isfile(config_file):
  sys.exit("'config.json' not found! Please add it and try again. Arbi.py file.")
else:
  with open(config_file) as file:
      config = json.load(file)

"""
Fetch arbitration data from CurrentMap.json and solNodes.json for embed construction.
"""
def get_arbitration_data():
    # Get the path of the directory containing the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the path of the parent directory
    parent_dir = os.path.dirname(current_dir)

    # Get the path of the JSON file in the parent directory
    map_json_file_path = os.path.join(parent_dir, config["current_map_json_file"])
    solnode_json_file_path = os.path.join(parent_dir, config["sol_nodes_json_file"])

    # Read data from CurrentMap.json
    with open(map_json_file_path, 'r') as f:
        current_map_data = json.load(f)
    start_time = current_map_data['start_time']
    end_time = current_map_data['end_time']
    sol_node = current_map_data['sol_node']

    # Read the data from the solNodes.json file
    with open(solnode_json_file_path, 'r') as f:
        sol_nodes_data = json.load(f)
    mission_data = sol_nodes_data[sol_node]
    enemy_type = mission_data['enemy']
    node = mission_data['node']
    planet = mission_data['planet']
    tileset = mission_data['tileset']
    mission_type = mission_data['type']
    dark_sector_bonus = None
    if mission_data['dark_sector']:
        dark_sector_bonus = mission_data['dark_sector_bonus']['resource']

    return start_time, end_time, enemy_type, node, planet, tileset, mission_type, dark_sector_bonus


"""
Return tier value and embed colour relative to the tier of mission.
"""
def get_mission_tier(node):
    s_tier = ["Cinxia", "Casta"]
    a_tier = ["Seimeni", "Sechura", "Hydron", "Odin", "Helene"]
    b_tier = ["Tessera", "Ose", "Hyf", "Outer Terminus"]
    c_tier = ["Larzac", "Sinai", "Sangeru", "Gulliver", "Alator", "Stephano", "Io", "Kala-azar", "Lares", "Lith", "Paimon", "Callisto", "Bellinus", "Cerberus", "Spear", "Umbriel"]
    d_tier = ["Coba", "Kadesh", "Romula", "Rhea", "Berehynia", "Oestrus", "Proteus", "Xini", "Cytherean", "Stöfler", "Taranis", "Mithra", "Gaia", "Caelus", "Akkad"]
    
    if node is None:
        return "F", 0xFF0000

    tier = "F"
    embed_color = 0xFF0000

    if node in s_tier:
        tier = "S"
        embed_color = 0x00fff3
    elif node in a_tier:
        tier = "A"
        embed_color = 0x00ff5a
    elif node in b_tier:
        tier = "B"
        embed_color = 0xfffc00
    elif node in c_tier:
        tier = "C"
        embed_color = 0xff9400
    elif node in d_tier:
        tier = "D"
        embed_color = 0xe95b00

    return tier, embed_color


"""
Create arbitration embed based on data.
"""
def create_arbi_embed(end_time, enemy_type, node, planet, tileset, mission_type, tier, embed_color, dark_sector_bonus):
    mission_name = f"{node} ({planet})"
    embed = discord.Embed(
        title=mission_name,
        color=embed_color
    )

    embed.add_field(
        name="Enemy", value=enemy_type, inline=False
    )

    embed.add_field(
        name="Mission type", value=mission_type, inline=False
    )

    embed.add_field(
        name="Arbi End", value=(f"Expiry: <t:{end_time}:R>"), inline=False
    )

    embed.add_field(
        name="Tier", value=f"**{tier}** tier", inline=True
    )

    if dark_sector_bonus is not None:
        embed.add_field(
            name="Resource Bonus", value=f"{dark_sector_bonus}%", inline=True
        )

    if enemy_type == "Infested":
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038479128480993424/1100459995398680700/Infested.png")
    elif enemy_type == "Corpus":
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038479128480993424/1100460526842171472/Corpus.png")
    elif enemy_type == "Grineer":
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038479128480993424/1100460022510649374/Grineer.png")
    else:
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/937368742462124042/1019362449977262120/arbi.png")

    embed.set_footer(text="Official Arbitration Goons Discord bot, developed by Basi.")
    
    return embed


class Arbis(commands.Cog, name="arbis"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="arbi",
        description="Get the current arbi."
    )
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def arbi(self, context: Context) -> None:
        global last_end_time

        data = get_arbitration_data()
        if data == None:
            print_fatal("ERROR: Missing data from get_arbitration_data()")
            return
        start_time, end_time, enemy_type, node, planet, tileset, mission_type, dark_sector_bonus = data

        tier_data = get_mission_tier(node)
        if None in tier_data:
            print_fatal("ERROR: Could not get arbitration tier.\n")
            return
        tier, embed_color = tier_data

        embed = create_arbi_embed(end_time, enemy_type, node, planet, tileset, mission_type, tier, embed_color, dark_sector_bonus)
        # channel = bot.get_channel(1100177413469646848) # dev channel
        # channel = bot.get_channel(1100371254592163890) # production channel
        
        """tier_roles = {
            "S": "1100498062843064381",
            "A": "1100498068832522240",
            "B": "1100498072024395916",
            "C": "1100498074226405616",
            "D": "1100508358852759683",
            "F": "1100498076461977650"
        }
        role_id = tier_roles.get(tier)
        if role_id:
            await context.send(f"<@&{role_id}>", embed=embed)"""
        
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="gear",
        description="Show gear used in META arbi."
    )
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def gear(self, context: Context) -> None:
        embed = discord.Embed(
            title="Arbitration Gear",
            color=0xff0000,
            description="""
            Current data suggests only the host needs market drop booster, doesn't hurt to have it incase host migration occurs or you start a squad. This stacks with drop chance blessing.

            :warning: You need to leave the relay once the squad has received a drop chance blessing then form up again once everyone has exited the relay. This ensures the blessing takes effect.
            """
        )

        embed.add_field(
            name="Ancient Healer",
            value=
            """
            Ancient healer grants 90% damage reduction, status and knockdown immunity to allies within 14m. If it absorbs radiation effects someone received it will become hostile for the duration and you will lose its buffs during that time. Highly recommend bringing if you're missing primed sure footed or just to soak damage (toxin can one shot you past waves 80+). Can also be placed in doorways to hold them open with hold position, helps with ai not getting stuck behind doors in certain locations.
            """,
            inline=False
        )

        embed.add_field(
            name="Nidus Specter",
            value=
            """
            Nidus specter will tether to you granting 1.28x strength bonus frequently. Zarr is technically better but swapping to Shedu until they fix the constant reload sound bug when specter is out of ammo and you’re full. Wisp can camp nidus or just use for motes.
            """,
            inline=False
        )

        embed.add_field(
            name="Protea Specter",
            value=
            """
            Protea specter casts dispensary when the player is below 70% energy/health or 70% ammo on primary or secondary (reserves). Lasts 25 seconds with a cooldown of 40 seconds after casting. With 3 power donations her base 25% at extra ammo drop will become 47.5% chance at 2 ammo drops. Have the specter hold position near the camp location, so they don’t follow you and drop dispensary away from the team.
            """,
            inline=False
        )

        embed.add_field(
            name="Large squad ammo restore",
            value=
            """
            Large squad ammo restore pulses every 7.5 seconds for a total of 4 times, totalling 30 seconds. Will restore 3 ammo for kuva ogris per pulse. After update 32: veilbreaker these will be very needed with base ammo pool reduced to 7…
            """,
            inline=False
        )

        embed.add_field(
            name="Railjack on-call crew",
            value=
            """
            Railjack on-call crew can also be spawned every so often to spout their nonsense and clean up occasional mobs. They might help you when the rest of the team is running around collecting vitus essence if you start to get overwhelmed. You'd think kuva ogris would be good on them but they hardly fire it, so Zarr is the go to here due to specters only having to reload one shell for full 5 magazine and good aoe damage.
            """,
            inline=False
        )

        embed.set_footer(text="Official Arbi Goons discord bot, developed by Basi.")
        await context.send(embed=embed)
        
    @commands.hybrid_command(
        name="holding",
        description="Shows how to hold missions."
    )
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def holding(self, context: Context) -> None:
        embed = discord.Embed(
            title="Holding Arbitrations",
            color=0xff0000,
        )

        embed.add_field(
            name="Method #1",
            value=
            """
            Way #1 is to have a friend in the party and que up the arbi mission, best to do it relay so u can get blessings while you hold. Make sure the friend knows not to vote to accept the mission so it does not start. If they leave the party that also removes the mission que. It is possible to have a 3rd person join and stay so the 2nd person can leave if they have to. This is the best way to hold the mission and can be done as long as needed. 
            *Also worth noting, if you change loadouts while in que, you lose the 300% arbi buff if you had it say on saryn+300 and you swapped to volt to link a build and swapped back to saryn. If you stay on the same loadout you get to keep the 300% buff.
            """,
            inline=False
        )

        embed.add_field(
            name="Method #2",
            value=
            """
            Way #2 is to change your region to one located geographically far away from your position, and to set the minimum squad ping requirement to 100. This method kind of sucks because you can still get random people joining you because you have to set the party to public in order to pause the mission que. I think this is due to other people attempting the same thing as you at the same time. You cannot leave the navigation menu or it cancels the que. 
            Using way #2 it is best to organize the squad via a discord thread and ensure correct roles and loadouts ahead of time before inviting anyone, including who is running enemy radar (1or2). Once everyone is ready to begin, invite one of them only, once they join the 20 second countdown will begin, you need to wait till the mission starts to send the invite to the other 2 players to avoid it canceling the mission. Make sure the squad knows NOT to use /join or to join from the friends list as it can cancel the mission.
            """,
            inline=False
        )

        embed.add_field(
            name="Method #2 cont.",
            value=
            """
            *Players that have already completed the arbitration(or have it marked as completed for going past wave 5 on defense or from failing) can still join another squad for the same one, they just cannot see it or que the mission for the squad. Another player can join temporarily just to que a mission if needed.
            """,
            inline=False
        )

        embed.set_footer(text="Official Arbi Goons discord bot, developed by Basi.")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="dd",
        description="Shows double dip."
    )
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def dd(self, context: Context) -> None:
        embed = discord.Embed(
            title="Douple Dipping",
            color=0xff0000,
            description=
            """
            (Discovered by: MeisterKleister)
            Doing this lets you get more out of a good defense tileset without having to risk going past 100w with defense operative. This can be good just in case the next arbi ends up not being a good tileset. For an Interception; this is not necessary due to the much slower enemy level scaling.

            1- Form a group and then go to relay for blessing.
            2- All 4 players leave the relay, after that group back up.
            3- Go back into relay, start arbi mission from the relay
            4- After 60-70w Extract 5-10 minutes before the hour changes the arbi.
            5- While inside relay and you will be able to do the arbi again for full 100w

            **If you exit the relay after doing it the first time it will remove the arbi from navigation.**

            This works out well for most defense tilesets, except for the Ice planet tileset which has 3 possible spawns, it's not worth trying to double dip unless all 4 players are trackin to keep pm's open for the 3 other members to be able to easily invite them as all 4 players attempt to find the good ice planet tile, then once someone finds it they send invites to the other 3. Don’t forget to set the party to “Friends only” or “Invite Only” to avoid randoms. Most prefer not to bother double dipping for Ice planet tile due to not getting the right tile the 2nd time around or if one of the players that gets it could potentially prove to have poor connection as a host.

            Steps 1-3 can be employed as a failsafe for all missions. In the event someone DCs early on or if someone has to leave, you’ll be able to do the arbi again.

            *Try to suppress the urge to press TAB to view kills and damage% during arbitrations, especially later on in the mission. Game client becomes clunky during longer missions and people will disconnect from host. I just wouldn’t press tab at all for defense, and for interception you can kinda get away with it during wave changes where you're capturing points. Another bug, If you are playing windowed or have multi monitor setup and your game pauses when you ALT TAB, then you will disconnect from the host if you do so for more than 7 seconds.

            """
        )

        embed.set_footer(text="Official Arbi Goons discord bot, developed by Basi.")
        await context.send(embed=embed)
    
    @commands.hybrid_command(
        name="tierlist",
        description="Shows tile tierlist."
    )
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def tierlist(self, context: Context) -> None:
        embed = discord.Embed(
            title="Arbitrations Tierlist",
            color=0xff0000,
        )

        embed.set_image(url="https://cdn.discordapp.com/attachments/1038479128480993424/1100804762934444174/ArbiTierlist.png")
        embed.set_footer(text="Official Arbi Goons discord bot, developed by Basi.")
        await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Arbis(bot))
