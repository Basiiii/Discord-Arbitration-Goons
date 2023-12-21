"""
Copyright © Basi

Github: https://github.com/basiiii
Website: https://basi.is-a.dev/
Discord: basi__

🏛️ Private discord bot for Warframe Arbitrations made with Discord.py.
https://discord.gg/arbitrations
"""

import json
import os
import sys
import discord
import traceback
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, CooldownMapping, BucketType
from fuzzywuzzy import fuzz, process
from termcolor import colored, cprint
from helpers.utils import print_fatal, print_warning, print_info

"""
Check if 'config.json' exists, and exit if it doesn't.
Otherwise, load its contents into the 'config' variable.
"""
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(script_dir, "config.json")

if not os.path.isfile(config_file):
  sys.exit("'config.json' not found! Please add it and try again. Maps.py file.")
else:
  with open(config_file) as file:
      config = json.load(file)

class Maps(commands.Cog, name="maps"):
    def __init__(self, bot):
      self.bot = bot
      self.maps_json_file = config["maps_json_file"]
      self.authorized_ids = config["authorized_ids"]
      # Cooldown variables
      self.user_cooldowns = CooldownMapping.from_cooldown(5, 1200, commands.BucketType.user)
      self.server_cooldowns = CooldownMapping.from_cooldown(30, 1200, commands.BucketType.guild)

    @commands.Cog.listener()
    async def on_ready(self):
        # Check if the JSON file exists
        if not os.path.exists(self.maps_json_file):
            print_fatal(f"Error: {self.maps_json_file} does not exist")
            return

        try:
            # Load the JSON file when the bot is ready
            with open(self.maps_json_file, "r") as file:
                self.map_holders = json.load(file)
        except json.JSONDecodeError:
            print_fatal(f"Error: Invalid JSON data in {self.maps_json_file}")

    @commands.hybrid_command(
        name="open",
        description="Open the map."
    )
    async def open(self, context: commands.Context, map_name: str = None, tier: str = None, rain: str = None) -> None:
        """
        Open the map.
        """
        user_id = context.author.id

        tier = tier.upper()

        if user_id in self.authorized_ids:
            if not map_name or not tier or not rain:
                await context.send("Please provide the name of the map, the type and if it's raining.")
                return

            # Define variations of "yes"
            positive_variations = ["yes", "ye", "ya", "+", "y", "yep", "yap"]
            # Define variations of "no"
            negative_variations = ["no", "na", "nah", "-", "n", "nope", "nop"]

            if rain.lower() in positive_variations:
                rain = "Yes"
            if rain.lower() in negative_variations:
                rain = "No"
            else:
                rain = "Unknown"

            # Compare the map_name with known map names using fuzzy matching
            map_names = ["Casta", "Seimeni"]
            best_match = process.extractOne(map_name, map_names)

            if best_match and best_match[1] >= 60:  # Consider a match if similarity is above 60%
                map_name = best_match[0]

            if not os.path.exists(self.maps_json_file):
                map_data = {}
            else:
                with open(self.maps_json_file, "r") as file:
                    map_data = json.load(file)

            if str(user_id) not in map_data or not map_data[str(user_id)]["status"]:
                # Update the map data with the user ID set to True, map name, and tier
                map_data[str(user_id)] = {
                    "status": True,
                    "map_name": map_name,
                    "tier": tier,
                    "embed_message_id": None
                }

                with open(self.maps_json_file, "w") as file:
                    json.dump(map_data, file, indent=4)

                await context.send(f"You are now holding the map {map_name} (Type {tier}).")
                
                # Send the embed to the specific channel
                channel_id = 1118853965300379668
                channel = self.bot.get_channel(channel_id)

                if channel:
                    enemy_types = {
                        "Casta": {
                            "enemy_type": "Grineer",
                            "ping_role": 1100775187416371310
                        },
                        "Seimeni": {
                            "enemy_type": "Infested",
                            "ping_role": 1100775116457115648
                        }
                    }

                    map_data_entry = enemy_types.get(map_name)
                    if map_data_entry:
                        enemy_type = map_data_entry["enemy_type"]
                        ping_role = map_data_entry["ping_role"]
                    else:
                        enemy_type = "Error with bot."
                        
                    embed = discord.Embed(
                        title=f"{map_name} - Ceres",
                        description=f"",
                        color=0xE02B2B
                    )
                    embed.add_field(
                        name="Enemy", value=enemy_type, inline=True
                    )
                    embed.add_field(
                        name="Rain", value=rain, inline=True
                    )
                    embed.add_field(
                        name="Type", value=f"**{tier}** type", inline=True
                    )
                    embed.add_field(
                        name="How to join",
                        value=f"""
                        Use the command ``/maps`` to request this map.
                        """,
                        inline=False
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
                    message = await channel.send(f"<@&{ping_role}> <@&1100498062843064381>",embed=embed)

                    # Update the embed_message_id in map_data
                    map_data[str(user_id)]["embed_message_id"] = message.id

                    log_channel_id = 1118962021266890843
                    log_channel = self.bot.get_channel(log_channel_id)
                    await log_channel.send(f"{map_name} (Type {tier}) opened by <@{user_id}>. Embed message ID: {message.id}")

                    with open(self.maps_json_file, "w") as file:
                        json.dump(map_data, file, indent=4)
            else:
                await context.send("You are already holding the map.")
        else:
            embed = discord.Embed(
                title="Unauthorized",
                description="You are not authorized to use this command.",
                color=discord.Color.red()
            )
            await context.send(embed=embed)


    @commands.hybrid_command(
        name="close",
        description="Close the map."
    )
    async def close(self, context: commands.Context) -> None:
        """
        Close the map.
        """
        user_id = context.author.id

        if user_id in self.authorized_ids:
            if not os.path.exists(self.maps_json_file):
                map_data = {}
            else:
                with open(self.maps_json_file, "r") as file:
                    map_data = json.load(file)

            if str(user_id) in map_data and map_data[str(user_id)]["status"]:
                # Retrieve the embed_message_id and map_name from map_data
                embed_message_id = map_data[str(user_id)].get("embed_message_id")
                map_name = map_data[str(user_id)].get("map_name")

                # Update the map data with the user ID set to False, remove embed_message_id, and clear map_name
                map_data[str(user_id)]["status"] = False
                map_data[str(user_id)]["embed_message_id"] = None
                map_data[str(user_id)]["map_name"] = None
                map_data[str(user_id)]["tier"] = None

                with open(self.maps_json_file, "w") as file:
                    json.dump(map_data, file, indent=4)

                await context.send("You have closed the map.")

                # Delete the message if embed_message_id is not None
                if embed_message_id:
                    channel_id = 1118853965300379668
                    channel = self.bot.get_channel(channel_id)

                    if channel:
                        try:
                            message = await channel.fetch_message(embed_message_id)
                            await message.delete()
                        except discord.NotFound:
                            print(f"Message with ID {embed_message_id} not found.")
            else:
                await context.send("You are not currently holding the map.")
        else:
            embed = discord.Embed(
                title="Unauthorized",
                description="You are not authorized to use this command.",
                color=discord.Color.red()
            )
            await context.send(embed=embed)


    @commands.command(
        name="closebyid",
        description="Close a map based on ID."
    )
    @commands.has_permissions(ban_members=True)
    async def close_by_id(self, context: commands.Context, user_id: int) -> None:
        """
        Close a map based on ID.
        """
        with open(self.maps_json_file, "r") as file:
            file_data = file.read().strip()
            if not file_data:
                # If the file is empty, initialize map_data as an empty dictionary
                map_data = {}
            else:
                map_data = json.loads(file_data)

        if str(user_id) in map_data and map_data[str(user_id)]:
            # Retrieve the embed_message_id and map_name from map_data
            embed_message_id = map_data[str(user_id)].get("embed_message_id")
            map_name = map_data[str(user_id)].get("map_name")

            # Update the map data with the user ID set to False, remove embed_message_id, and clear map_name
            map_data[str(user_id)] = {
                "status": False
            }

            with open(self.maps_json_file, "w") as file:
                json.dump(map_data, file, indent=4)

            await context.send("You have closed the map.")

            # Delete the message if embed_message_id is not None
            if embed_message_id:
                channel_id = 1118853965300379668
                channel = self.bot.get_channel(channel_id)

                if channel:
                    message = await channel.fetch_message(embed_message_id)
                    if message:
                        await message.delete()
                    else:
                        print_fatal(f"Message with ID {embed_message_id} not found.")
        else:
            await context.send("The specified user ID is not holding a map.")

    @commands.command(
        name="overwrite_maps",
        description="Overwrite the maps.json file with new data."
    )
    @commands.check_any(commands.has_role("Arbmin"))
    async def overwrite_maps(self, context: commands.Context, *, json_data: str) -> None:
        """
        Overwrite the maps.json file with new data.
        """
        # Parse the JSON data
        try:
            new_data = json.loads(json_data)
        except json.JSONDecodeError:
            await context.send("Invalid JSON data.")
            return

        # Write the new data to the maps.json file
        try:
            with open("maps.json", "w") as file:
                json.dump(new_data, file, indent=4)
        except IOError:
            await context.send("Error writing to the maps.json file.")
            return

        await context.send("The maps.json file has been successfully overwritten with new data.")

    @commands.hybrid_command(
        name="confirmation",
        description="Confirm that you've read the arbi map sharing information."
    )
    async def confirmation(self, context: commands.Context) -> None:
        """
        Confirm that you've read the rules.
        """
        user_id = context.author.id

        # Load confirmation data from the JSON file
        with open("confirmation.json", "r") as file:
            confirmation_data = json.load(file)

        # Check if the user has already confirmed
        if str(user_id) in confirmation_data:
            await context.send("You have already confirmed that you've read the information.")
            return

        # Add the user's confirmation to the data
        confirmation_data[str(user_id)] = True

        # Save the updated confirmation data to the JSON file
        with open("confirmation.json", "w") as file:
            json.dump(confirmation_data, file)

        await context.send("Thank you for confirming that you've read the rules! Have fun farming.")


    @commands.hybrid_command(
        name="maps",
        description="Check the availability of maps."
    )
    async def maps(self, context: commands.Context, ign=None, map_choice: str = "") -> None:
        """
        Check the availability of maps.
        """
        user_id = context.author.id
        guild_id = context.guild.id

        # Check if the user has confirmed by checking the JSON file
        with open("confirmation.json", "r") as file:
            confirmation_data = json.load(file)

        if str(user_id) not in confirmation_data:
            await context.send("You must read the information in https://discord.com/channels/1100168231207059456/1118853965300379668.\n\nOnce you've read the information, confirm by using the ``/confirmation`` command!")
            return

        # Check if the user has the required roles
        required_roles = ["Arbi Goon", "Arbimaster", "Arbivanced"]
        has_required_roles = any(role.name in required_roles for role in context.author.roles)
        if not has_required_roles:
            await context.send("You must be **arbivanced** or higher to use this command! https://discord.com/channels/1100168231207059456/1100172738339033100")
            return

        if ign is None:
            await context.send("You did not give your IGN. Please read and follow the correct format.")
            return

        if not map_choice:
            await context.send("Please choose a map (Casta or Seimeni).")
            return

        # Check if the chosen map is available
        if map_choice.lower() not in ["casta", "seimeni"]:
            await context.send("Invalid map choice. Please choose between Casta and Seimeni.")
            return

        # Check if the chosen map is available in the JSON
        with open(self.maps_json_file, "r") as file:
            file_data = file.read().strip()
            if not file_data:
                # If the file is empty, initialize map_data as an empty dictionary
                map_data = {}
            else:
                map_data = json.loads(file_data)

        holders = [holder_id for holder_id, map_entry in map_data.items() if map_entry["status"] and map_entry["map_name"].lower() == map_choice.lower()]

        if not holders:
            await context.send(f"There are no {map_choice} maps currently available.")
            return

        # Check user cooldown
        user_bucket = self.user_cooldowns.get_bucket(context.message)
        retry_after_user = user_bucket.update_rate_limit()
        if retry_after_user:
            print_info(f"User ID: {user_id} is on cooldown. Retry after {retry_after_user} seconds.")
            await context.send(f"Command on cooldown. Please wait {retry_after_user} seconds before using it again.")
            return

        # Check server cooldown
        server_bucket = self.server_cooldowns.get_bucket(context.message)
        retry_after_server = server_bucket.update_rate_limit()
        if retry_after_server:
            print_info(f"Server ID: {guild_id} is on cooldown. Retry after {retry_after_server} seconds.")
            await context.send(f"Command on cooldown. Please wait {retry_after_server} seconds before using it again.")
            return

        # Log message
        log_message = f"User <@{user_id}> has requested a map. They claimed to have the IGN: {ign}"
        log_channel_id = 1118962021266890843
        log_channel = self.bot.get_channel(log_channel_id)
        # Send DMs to map holders
        confirmation_message = "The map holders have been notified. Please wait for their reply."
        for holder_id in holders:
            try:
                holder_user = await self.bot.fetch_user(holder_id)
                if holder_user:
                    embed = discord.Embed(
                        title="Map Request",
                        description=f"**You received a map request from: <@{user_id}>** ```/inv {ign}```",
                        color=discord.Color.green()
                    )
                    await holder_user.send(embed=embed)
            except Exception as e:
                print_warning(f"Error sending DM to user ID: {holder_id}")
                traceback.print_exc()  # Print the full error traceback

        await log_channel.send(log_message)
        await context.send(confirmation_message)

async def setup(bot):
    await bot.add_cog(Maps(bot))
