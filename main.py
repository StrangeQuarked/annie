#Created by Chaedr (@chaedr_) and Quark (@StrangeQuarked).
import discord
import os
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix=['a.', "annie "], case_insensitive=True)

@bot.event
async def on_ready():
  print("I'm in")
  print(bot.user)
#code below loads all cogs, i copied it from a template. all cogs need to be in this list so that the bot will load them, and you have to put 'cogs.' in front of the file name b/c of the file path -c
extensions = [
	'cogs.gearcalcs',
  'cogs.randomizers'
]
if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

@bot.command()
async def commands(ctx):
  await ctx.send("Current list of commands:\n`a.randmode` gives a random mode.\n`a.randmap [number of maps]` gives random maps.\n`a.maplist (number of maps)` generates a random maplist of up to 64 maps.\n`a.gearcalc (ability) (amount)` calculates the effect of a specified number of ability chunks. () denotes required parameters, [] optional parameters.")

@bot.command()
async def weaponglossary(ctx):
  FullWeaponNames = ["Splattershot Jr.", "Splattershot", "Splash-o-Matic", "Sploosh-o-Matic", "N-ZAP", "Aerospray", ".52 Gal", "Splattershot Pro", "Squeezer", ".96 Gal", "L-3 Nozzlenose", "H-3 Nozzlenose", "Jet Squelcher", "Luna Blaster", "Blaster", "Range Blaster", "Clash Blaster", "Rapid Blaster", "Rapid Blaster Pro", "Roller", "Carbon Roller", "Flingza Roller", "Dynamo Roller", "Inkbrush", "Octobrush", "Slosher", "Tri-slosher", "Sloshing Machine", "Bloblobber", "Explosher", "Squiffer", "Splat Charger", "Splatterscope", "E-liter", "E-liter Scope", "Bamboozler", "Goo Tuber", "Mini Splatling", "Heavy Splatling", "Nautilus", "Hydra Splatling", "Ballpoint Splatling", "Dapple Dualies", "Splat Dualies", "Tetra Dualies", "Glooga Dualies", "Dualie Squelchers", "Undercover Brella", "Splat Brella", "Tenta Brella", "Rainmaker"]
  ShortWeaponNames = ["jr", "shot", "splash", "sploosh", "nzap", "aerospray", "52", "pro", "squeezer", "96", "l-3", "h-3", "jet", "luna", "blaster", "range-blaster", "clash", "rapid-blaster", "rapid-pro", "roller", "carbon", "flingza", "dynamo", "inkbrush", "octobrush", "slosher", "tri", "machine", "bloblobber", "explosher", "squiffer", "charger", "scope", "eliter", "eliter-scope", "bamboozler", "gootuber", "mini", "heavy", "nautilus", "hydra", "ballpoint", "dapples", "dualies", "tetras", "gloogas", "dualie-squelchers", "undercover", "brella", "tent", "rainmaker"]
  output = "```The following is a glossary of full weapon names to the shortened names used for bot commands. The shortened names must be input exactly as they are shown in the glossary, including the hyphens.\n"
  output2 = "```"
  for x in range(24):#uses 2 for loops since the glossary must be sent in 2 messages to be under 2000 characters
    output += f"Full weapon name: {FullWeaponNames[x]}. Shortened name: '{ShortWeaponNames[x]}'.\n"
  for x in range(26):
    output2 += f"Full weapon name: {FullWeaponNames[x+25]}. Shortened name: '{ShortWeaponNames[x+25]}'.\n"
  await ctx.send(output+"```")
  await ctx.send(output2+"```")

@bot.command()
async def abilityglossary(ctx):
  await ctx.send("```List of valid ability abbreviations: 'bdef' and 'bdx' for Bomb Defense Up DX, 'bpu' for Sub(Bomb) Power Up, 'ism' for Ink Saver Main, 'iss' for Ink Saver Sub, 'mpu' for Main Power Up, 'qr' for Quick Respawn, 'qsj' for Quick Super Jump, 'rec' for Ink Recovery Up, 'res' for Ink Resistance Up, 'rsu' for Run Speed Up, 'ssu' for Swim Speed Up, 'ss' for Special Saver, 'scu' for Special Charge Up,  'spu' for Special Power Up.\nValid abbreviations for gear-exclusive abilities (i.e. Comeback): 'opening-gambit' or 'og' for Opening Gambit, 'comeback' or 'cbk' for Comeback, 'last-ditch-effort' or 'lde' for Last Ditch Effort, 'ninja-squid' or 'ns' for Ninja Squid.```")

@bot.command()
async def subspecialglossary(ctx):
  await ctx.send("```List of valid sub weapon names: 'splat-bomb', 'suction-bomb', 'autobomb', 'curling-bomb', 'burst-bomb', 'fizzy-bomb', 'beakon', 'mine', 'wall', 'torpedo', 'toxic-mist', 'sensor', 'sprinkler'.\nList of valid special weapon names: 'baller', 'curling-launcher', 'suction-launcher', 'splat-launcher', 'autobomb-launcher', 'burst-launcher', 'booyah', 'bubbles', 'inkjet', 'armor', 'storm', 'rain', 'missiles', 'ray', 'stamp', 'splashdown'.\nSub and special weapon names are case sensitive and hyphens are required where shown.```")

@bot.command()
async def creators(ctx):
  await ctx.send("Annie was created by Chaedr and Quark. They can be found on Twitter at @chaedr_ and @StrangeQuarked, respectively.")

@bot.command()
async def selfcare(ctx):
  await ctx.send("Please make sure you have hydrated, eaten sufficient food, moved around if you have been sitting for a while, slept if you are tired, taken any necessary medication and done any other actions needed to take care of yourself. Self-care is very important. I might be a robot but I still care about you :).")


#things for livin
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)