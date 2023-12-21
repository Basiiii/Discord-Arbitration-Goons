""""
Copyright © Basi 2023
https://github.com/basiiii
https://basi.is-a.dev/
Basi#1056

🏛️ Private discord bot for Warframe Arbitrations made with Discord.py.
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

# Dictionary of tiles and IDs
roles = {
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
    'Tyana Pass': "1113634607456333895"
}


class Roles(commands.Cog, name="roles"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="node",
        description="Get a specific node role.",
    )
    async def tile(self, context: Context, *, missionname) -> None:
        """
        Get a specific node role.

        :param context: The hybrid command context.
        """
        role_name_lower = missionname.lower()
        matched_role = next((r for r in roles.keys() if r.lower() == role_name_lower), None)

        if matched_role:
            role_id = roles[matched_role]
            role = discord.utils.get(context.guild.roles, id=int(role_id))

            if role in context.author.roles:
                await context.author.remove_roles(role)
                await context.send(f"Role {matched_role} has been removed from {context.author.mention}")    
            else:
                await context.author.add_roles(role)
                await context.send(f"Role {matched_role} has been added to {context.author.mention}")
        else:
            await context.send(f"Role {missionname} does not exist")

async def setup(bot):
    await bot.add_cog(Roles(bot))
