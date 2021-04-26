import random
from discord.ext import commands
from cogs import mapweights


class Randomizers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.maps = [
            "Ancho-V Games",
            "Arowana Mall",
            "Blackbelly Skatepark",
            "Camp Triggerfish",
            "Goby Arena",
            "Humpback Pump Track",
            "Inkblot Art Academy",
            "Kelp Dome",
            "MakoMart",
            "Manta Maria",
            "Moray Towers",
            "Musselforge Fitness",
            "New Albacore Hotel",
            "Piranha Pit",
            "Port Mackerel",
            "Shellendorf Institute",
            "Skipper Pavilion",
            "Snapper Canal",
            "Starfish Mainstage",
            "Sturgeon Shipyard",
            "The Reef",
            "Wahoo World",
            "Walleye Warehouse",
        ]
        self.modes = ["Splat Zones", "Clam Blitz", "Tower Control", "Rainmaker"]

    @commands.command()
    async def randmap(self, ctx, amnt=1):  # sends a random map
        gen = []  # stands for generated
        for x in range(amnt):
            gen.append(self.maps[random.randint(0, len(self.maps) - 1)])
        result = "```"
        for index in range(len(gen)):
            result += f"{index + 1}. {gen[index]}\n"  # numbered list
        await ctx.send(result + "```")
        # await ctx.send('{} random maps: {}'.format(len(gen), ', '.join(gen))) #i should make this print a numbered list for readability

    @commands.command()
    async def randmode(self, ctx):  # sends a random mode
        gen = self.modes[random.randint(0, len(self.modes) - 1)]
        await ctx.send("Selected Mode: {}".format(gen))

    @commands.command()
    async def maplist(self, ctx, amount=1, pool=""):  # generates a random maplist
        if amount >= 60:
            await ctx.send("Too many maps. Maximum maplist size of 59")
        else:
            CreatedList = []
            if pool == "syzygy":
                maps = random.choices(
                    self.maps, weights=self.mapweights["syzygy"], k=amount
                )
                for x in range(amount):
                    genmode = self.modes[random.randint(0, len(self.modes) - 1)]
                    CreatedList.append(genmode + " on " + maps[x - 1])
            elif pool == "cursed":
                maps = random.choices(
                    self.maps, weights=self.mapweights["cursed"], k=amount
                )
                for x in range(amount):
                    genmode = self.modes[random.randint(0, len(self.modes) - 1)]
                    CreatedList.append(genmode + " on " + maps[x - 1])
            elif pool == "quark":
                CreatedList = random.choices(
                    mapweights.MapModes, weights=mapweights.Quark, k=amount
                )
            else:
                for x in range(amount):
                    genmode = self.modes[random.randint(0, len(self.modes) - 1)]
                    genmap = self.maps[random.randint(0, len(self.maps) - 1)]
                    CreatedList.append(genmode + " on " + genmap)
            result = "```"
            for index in range(len(CreatedList)):
                result += f"{index + 1}. {CreatedList[index]}\n"
            try:
                await ctx.send(result + "```")
            except:
                await ctx.send(
                    "Maplist over 2000 characters. Try a smaller maplist size."
                )


def setup(bot):
    bot.add_cog(Randomizers(bot))
