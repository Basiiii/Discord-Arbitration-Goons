"""
Copyright © Basi

Github: https://github.com/basiiii
Website: https://basi.is-a.dev/
Discord: basi__

🏛️ Private discord bot for Warframe Arbitrations made with Discord.py.
https://discord.gg/arbitrations
"""

import asyncio
import datetime
import json
import os
import platform
import sys

from fuzzywuzzy import fuzz, process
from dateutil.parser import isoparse

from helpers.utils import print_fatal, print_warning, print_info

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

import requests

"""
Defining tier lists for arbitrations & last end_time value of arbitration to prevent duplicates.

S, A, B, C and D tiers.
Default to F tier.
"""
s_tier = ["Cinxia", "Casta", "Seimeni"]
a_tier = ["Sechura", "Hydron", "Odin", "Helene"]
b_tier = ["Tessera", "Ose", "Hyf", "Outer Terminus"]
c_tier = ["Larzac", "Sinai", "Sangeru", "Gulliver", "Alator", "Stephano", "Io", "Kala-azar", "Lares", "Lith", "Paimon", "Callisto", "Bellinus", "Cerberus", "Spear", "Umbriel"]
d_tier = ["Coba", "Kadesh", "Romula", "Rhea", "Berehynia", "Oestrus", "Proteus", "Xini", "Cytherean", "Stöfler", "Taranis", "Mithra", "Gaia", "Caelus", "Akkad"]
last_end_time = None
use_api = False

"""
Check if 'config.json' exists, and exit if it doesn't.
Otherwise, load its contents into the 'config' variable.
"""
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, "config.json")

if not os.path.isfile(config_file):
  sys.exit("'config.json' not found! Please add it and try again.")
else:
  with open(config_file) as file:
      config = json.load(file)

"""
Channel ID's
"""
log_channel_id = config["log_channel_id"]
announcements_channel_id = config["announcement_channel_id"]

"""
Debug mode
"""
if config["debug_mode"] == "true":
    debug_mode = True
else:
    debug_mode = False

"""
Core JSON files
"""
maps_path = os.path.join(script_dir, config["maps_json_file"])
confirmation_path = os.path.join(script_dir, config["user_confirmation_json_file"])
sol_nodes_path = os.path.join(script_dir, config["sol_nodes_json_file"])
map_path = os.path.join(script_dir, config["current_map_json_file"])

"""
Authorized ID's
"""
authorized_ids = config["authorized_ids"]

"""
Load maps file.
"""
if not os.path.exists(maps_path):
    raise FileNotFoundError(f"Error: {maps_path} does not exist")

try:
    with open(maps_path, "r") as file:
        map_holders = json.load(file)
except json.JSONDecodeError as e:
    raise ValueError(f"Error: Invalid JSON data in {maps_path}") from e

"""
Define Discord intents.
"""
intents = discord.Intents.default()
# intents = discord.Intents.all()
intents.message_content = True

"""
Create Discord bot instance with specified command prefix and intents.
If config.json file has a "prefix" key, it will be used as the command prefix.
Otherwise, the bot will be invoked using a mention.
"""
bot = Bot(command_prefix=commands.when_mentioned_or(
    config["prefix"]), intents=intents, help_command=None)

"""
Create a bot variable to access the config file in cogs so that you don't need to import it every time.

The config is available using the following code:
- bot.config # In this file
- self.bot.config # In cogs
"""
bot.config = config

@bot.event
async def on_ready() -> None:
    """
    Event handler for when the bot is ready to run.
    """
    print_info("\nLoading bot:")
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("Arbitration Goons bot is now online.")
    if config["sync_commands_globally"]:
        print_info("\nSyncing commands globally...")
        await bot.tree.sync()
    print_info("\nStarting tasks:")
    print("Starting arbitration notification task...")
    arbi_task.start()
    print("Notification task is now running every 30 seconds.\n")

async def load_extensions():
    """
    Loads cogs from the cogs folder.
    """
    print_info("\nLoading cogs:")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Cog {filename[:-3]} loaded successfully.")

"""
Get last_end_time from last sent arbi.
"""
async def check_last_sent():
    channel_id = announcements_channel_id
    channel = bot.get_channel(channel_id)  # Get the TextChannel object

    # Fetch the most recent message in the channel
    async for message in channel.history(limit=1):
        if debug_mode:
            print(message)

        # Check if the message has an embed
        if message.embeds:
            if debug_mode:
                print(message.embeds)
            for embed in message.embeds:
                if debug_mode:
                    print(embed.to_dict())
                # Check if the embed has the expected field
                for field in embed.fields:
                    if field.name == "Arbi End":
                        end_time_value = field.value
                        # Extract the end_time value from the field value
                        end_time = int(end_time_value.split("<t:", 1)[1].split(":", 1)[0])
                        return end_time

    return None  # Return None if no valid end_time is found

"""
Log arbi to a JSON.
"""
def log_data_to_json(end_time, enemy_type, node, planet, tileset, mission_type, tier, embed_color, dark_sector_bonus):
    log_entry = {
        "end_time": end_time,
        "enemy_type": enemy_type,
        "node": node,
        "planet": planet,
        "tileset": tileset,
        "mission_type": mission_type,
        "tier": tier,
        "embed_color": embed_color,
        "dark_sector_bonus": dark_sector_bonus
    }

    try:
        with open("arbi_maps.json", "r") as file:
            log_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        log_data = {}

    # Generate a unique key for each log entry
    log_key = f"arbi{len(log_data) + 1}"
    log_data[log_key] = log_entry

    with open("arbi_maps.json", "w") as file:
        json.dump(log_data, file)

"""
Fetch arbitration data from current map JSON file and sol nodes JSON file or API for embed construction.
"""
async def get_arbitration_data():
    if use_api: # Fetch from API
        await asyncio.sleep(50)
        print_warning("Using API data.")
        try:
            response = requests.get("https://api.warframestat.us/pc/arbitration/")
            if response.status_code == 200:
                data = response.json()
                expired = data.get("expired")
                # if expired:
                #     print_fatal("Arbitration has expired.")
                #     return None, None, None, None, None, None, None, None

                start_api_timestamp = data.get("activation")
                start_api_datetime = datetime.datetime.fromisoformat(start_api_timestamp.replace("Z", "+00:00"))
                start_time = int(start_api_datetime.timestamp())

                end_api_timestamp = data.get("expiry")
                end_api_datetime = datetime.datetime.fromisoformat(end_api_timestamp.replace("Z", "+00:00"))
                end_time = int(end_api_datetime.timestamp())

                enemy_type = data.get("enemy")
                
                node_fetch = data.get("node")
                split_node = node_fetch.split("(", 1)
                node = split_node[0].strip()

                planet_fetch = data.get("node")
                start_index = planet_fetch.index("(") + 1
                end_index = planet_fetch.index(")")
                planet = planet_fetch[start_index:end_index]
                
                tileset = data.get("typeKey")
                mission_type = data.get("typeKey")
                dark_sector_bonus = None

                return start_time, end_time, enemy_type, node, planet, tileset, mission_type, dark_sector_bonus
            else:
                print("Failed to fetch data from the API.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from the API: {e}")

        # Set all values to None in case of a fatal error
        return None, None, None, None, None, None, None, None
    else: # Fetch from log JSON
        if debug_mode:
            print_info("Using log data.")
            
        if os.path.exists(map_path):
            with open(map_path, 'r') as f:
                current_map_data = json.load(f)
        else:
            current_map_data = {}
            with open(map_path, 'w') as f:
                json.dump(current_map_data, f)
        
        try:
            start_time = current_map_data['start_time']
            end_time = current_map_data['end_time']
            sol_node = current_map_data['sol_node']
            
            if debug_mode:
                print_info(f"Fetched node:{sol_node}")

            with open(sol_nodes_path, 'r') as f:
                sol_nodes_data = json.load(f)
            mission_data = sol_nodes_data[sol_node]
            enemy_type = mission_data['enemy']
            node = mission_data['node']
            planet = mission_data['planet']
            tileset = mission_data['tileset']
            mission_type = mission_data['type']
            # print(mission_data['dark_sector'])
            dark_sector_bonus = None
            if mission_data['dark_sector']:
                dark_sector_bonus = mission_data['dark_sector_bonus']['resource']
                
            if debug_mode:
                print_info(f"Tile is {tileset}")
                
        except KeyError:
            print_fatal("There was a key error, the specified key does not exist.")
            return None, None, None, None, None, None, None, None
            
        return start_time, end_time, enemy_type, node, planet, tileset, mission_type, dark_sector_bonus

"""
Return tier value and embed colour relative to the tier of mission.
"""
def get_mission_tier(node):
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

"""
Send arbitration embed and ping the respective tier role.
"""
async def send_arbitration(node_id, tier, channel, embed):
    tier_roles = {
        "S": "1100498062843064381",
        "A": "1100498068832522240",
        "B": "1100498072024395916",
        "C": "1100498074226405616",
        "D": "1100508358852759683",
        "F": "1100498076461977650"
    }
    role_id = tier_roles.get(tier)
    if role_id and node_id:
        message = await channel.send(f"<@&{role_id}> <@&{node_id}>", embed=embed)
    elif role_id and not node_id:
        message = await channel.send(f"<@&{role_id}>", embed=embed)
    else:
        message = await channel.send(embed=embed)
    
    # Publish the message if the channel type is 'NEWS'
    if channel.type == discord.ChannelType.news and not message.flags.crossposted:
        url = f"https://discord.com/api/v9/channels/{channel.id}/messages/{message.id}/crosspost"
        token = config["token"]
        headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print_info("New arbitration published to channel.")
        else:
            print_fatal(f"Failed to publish arbitration: {response.content}")
    else:
        print_info("New arbitration sent to channel.")

"""
Get discord role ID for the Node.
"""
async def get_node_id(node):
    node_dict = {
        'Romula': "1113784663782195313",
        'Malva': "1113784667234127933",
        'Memphis': "1113784670430175262",
        'Zeugma': "1113784673487826995",
        'Caracol': "1113784676553871400",
        'Piscinas': "1113784680127410196",
        'Amarna': "1113784683902287872",
        'Sangeru': "1113784687320641556",
        'Ur': "1113784690810294333",
        'Assur': "1113784694006349834",
        'Akkad': "1113784697064005692",
        'Zabala': "1113784700041969714",
        'Coba': "1113784703120584724",
        'Yursa': "1113784706144686090",
        'Kelashin': "1113784709181349948",
        'Gabii': "1113784712268365884",
        'Hieracon': "1113784715472818216",
        'Tikal': "1113784718538850454",
        'Sinai': "1113784722275958855",
        'Cameria': "1113784726117961738",
        'Cholistan': "1113784729599230053",
        'Kadesh': "1113784732824641676",
        'Wahiba': "1113784735878098944",
        'Mars': "1113784738986066030",
        'Void': "1113784742031130714",
        'Ganymede': "1113784745382387732",
        'Gulliver': "1113784749006258257",
        'Stickney': "1113784752147808297",
        'Elara': "1113784755272568832",
        'Kiliken': "1113784758527336610",
        'Alator': "1113784762432245790",
        'Laomedeia': "1113784765460521020",
        'Stephano': "1113784768425902150",
        'V Prime': "1113784771391262750",
        'Io': "1113784774906105906",
        'Lares': "1113784778525777931",
        'Draco': "1113784781633749022",
        'Augustus': "1113784784724951090",
        'Kala-azar': "1113784787895844904",
        'Nimus': "1113784791087714445",
        'Proteus': "1113784794740953088",
        'Xini': "1113784798415175690",
        'Kappa': "1113784801409900634",
        'Rhea': "1113784804501110814",
        'Berehynia': "1113784807546163201",
        'Selkie': "1113784811102949457",
        'Ose': "1113784814269628447",
        'Paimon': "1113784817629270128",
        'Valefor': "1113784820955349062",
        'Tessera': "1113784824189165568",
        'Cytherean': "1113784827934679151",
        'Lith': "1113784831113961522",
        'Olympus': "1113784834310021242",
        'Tycho': "1113784837577379980",
        'Stöfler': "1113784840882495498",
        'Apollo': "1113784844137275533",
        'Everest': "1113784847656288377",
        'Taranis': "1113784851338891274",
        'Ani': "1113784854551724164",
        'Belenus': "1113784857529692182",
        'Mot': "1113784860843192341",
        'Mithra': "1113784863804375162",
        'Cerberus': "1113784866765549628",
        'Spear': "1113784870074855445",
        'Despina': "1113784873530962001",
        'Umbriel': "1113784876634734643",
        'Ophelia': "1113784879759507457",
        'Terrorem': "1113784882963947520",
        'Outer Terminus': "1113784885937709077",
        'Taveuni': "1113784889343479848",
        'Tamu': "1113784892661178398",
        'Palus': "1113784895966289930",
        'Gaia': "1113784899040727142",
        'Apollodorus': "1113784902505213952",
        'Titan': "1113784906095525898",
        'Casta': "1100775187416371310",
        'Cinxia': "1100775220450693190",
        'Helene': "1100775083955458118",
        'Hydron': "1100775036677275688",
        'Odin': "1100775154952450270",
        'Sechura': "1100774991743688855",
        'Seimeni': "1100775116457115648",
        'Callisto': "1100779444450373726",
        'Larzac': "1100782407189274784",
        'Hyf': "1100782443319001169",
        'Tyana Pass': "1113634607456333895",
        'Munio': "1184871637347209227",
        'Persto': "1184871712152633464",
        'Cambire': "1184871782524665906"
    }

    return node_dict.get(node, None)

"""
Construct and send arbitration embed to notification channel.
"""
@tasks.loop(seconds=30)
async def arbi_task():
    print("")
    try:
        global last_end_time
        print_info("Checking for new arbitration...")

        # After restart, the bot will check last sent arbi and initialize last_end_time
        if last_end_time == None:
            last_end_time = await check_last_sent()
            
            if debug_mode:
                print_info(f"LAST EMBED TIMESTAMP FOUND: {last_end_time}")

        data = await get_arbitration_data()
        if all(value is None for value in data):
            print_fatal("ERROR: Missing data from get_arbitration_data()")
            return

        start_time, end_time, enemy_type, node, planet, tileset, mission_type, dark_sector_bonus = data
        if end_time == last_end_time:
            print_warning("Arbitration is a duplicate. Not sending.")
            return

        last_end_time = end_time  # Update last_end_time

        tier_data = get_mission_tier(node)
        if None in tier_data:
            print_fatal("ERROR: Could not get arbitration tier.\n")
            return
            
        tier, embed_color = tier_data

        embed = create_arbi_embed(end_time, enemy_type, node, planet, tileset, mission_type, tier, embed_color, dark_sector_bonus)
        
        channel = bot.get_channel(announcements_channel_id)
        
        node_id = await get_node_id(node)

        await send_arbitration(node_id, tier, channel, embed)

        log_data_to_json(end_time, enemy_type, node, planet, tileset, mission_type, tier, embed_color, dark_sector_bonus)
            
        await bot.change_presence(activity=discord.Game(f"Current Arbi: {node} ({planet})"))
    except Exception as e:
        print(f"An error occurred during announcement task execution: {e}")

async def main():
    """
    Executes the bot.
    """
    await load_extensions()
    await bot.start(config["token"])

asyncio.run(main())
