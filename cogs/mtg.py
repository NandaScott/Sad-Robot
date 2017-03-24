import asyncio
import aiohttp
import json
import discord
from discord.ext import commands

class Mtg():
    def __init__(self, bot):
        self.bot = bot
        loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=loop)

    async def get_json(self, url, **kwargs):
        async with self.session.get(url, **kwargs) as response:
            assert response.status == 200
            return await response.read()

    @commands.command(pass_context=True)
    async def mtg(self, message : str, ctx):
        try:
            data = await self.get_json(url='http://api.scryfall.com/cards/named?', params={'fuzzy': ctx})
            card = json.loads(data.decode('utf-8'))
            msg = discord.Embed(url=card['scryfall_uri'], color=discord.Color(0x1b6f9))
            msg.set_image(url=card['image_uri'])
            msg.title = "**" + card['name'] + "**"
            await self.bot.say(embed=msg)
        except Exception:
            await self.bot.say("Sorry, couldn't find that card. Check your spelling or syntax.")
            return

def setup(bot):
    bot.add_cog(Mtg(bot))
