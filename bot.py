import discord, logging, aiohttp
from secret import token
from discord.ext import commands
description = '''
A bot that was made to practice my python and make a cool function for my discord server.
'''

bot = commands.Bot(command_prefix='?', description=description)
bot.aiohttp_session = aiohttp.ClientSession(loop=bot.loop)
#Manages what extensions are required.
startup_extensions = [
    "cogs.mtg",
    "cogs.rng",
    "cogs.meta",
    "cogs.fun",
    "cogs.admin"
]

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')



if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)
