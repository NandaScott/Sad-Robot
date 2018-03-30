import discord, logging, aiohttp
from secret import token
from discord.ext import commands
import asyncio, time, re

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

async def getRequest(url, **kwargs):
    async with bot.aiohttp_session.get(url, **kwargs) as response:
        return await response.json()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    matched = re.findall(r'\[\[\b[\w\s\'\.]+\b\]\]', message.content)

    for name in matched:
        asyncio.sleep(0.1)
        startTimer = time.monotonic()
        card = await getRequest(url='https://api.scryfall.com/cards/named?', params={'fuzzy':name})
        endTimer = time.monotonic()
        f = endTimer - startTimer

        if card['object'] == 'error':
            await bot.send_message(message.channel, re.sub(r'\(|\'|,|\)+', card['details']))
            continue

        if 'card_faces' in card:
            for entry in card['card_faces']:
                msg = discord.Embed(
                    title="**{}**".format(entry['name']),
                    url=card['scryfall_uri'],
                    color=discord.Color(0x1b6f9)
                )
                msg.set_image(url=entry['image_uris']['normal'])
                msg.footer(text='Fetch took: {} seconds.'.format('%.3f' % f))
                await bot.send_message(message.channel, embed=msg)
            return

        msg = discord.Embed(
            title='**{}**'.format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9)
        )

        msg.set_footer(text='Fetch took: {} seconds.'.format('%.3f' % f))
        msg.set_image(url=card['image_uris']['normal'])
        await bot.send_message(message.channel, embed=msg)



if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)
