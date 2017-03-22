import aiohttp
import json
import discord
from discord.ext import commands

class Mtg():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mtg(message : str, ctx):
        print("Requesting card: " + str(ctx))
        async with aiohttp.ClientSession() as session:
            fetch = session.get('http://api.scryfall.com/cards/named?fuzzy=ctx')
        msg = discord.Embed(url=fetch['data'][0]['scryfall_uri'])
        msg.set_image(url=fetch['data'][0]['image_uri'])
        await self.bot.say(embed=msg)

def setup(bot):
    bot.add_cog(Mtg(bot))
