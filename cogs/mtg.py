import aiohttp
import json
import discord
from discord.ext import commands

class Mtg():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mtg(self, message : str, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.scryfall.com/cards/named?', params={'fuzzy':ctx}) as resp:
                    card = resp.json()
        msg = discord.Embed(url=card.next(['scryfall_uri']), color=discord.Color(0x1b6f9))
        msg.set_image(url=card.next(['image_uri']))
        await self.bot.say(embed=msg)

def setup(bot):
    bot.add_cog(Mtg(bot))
