from discord.ext import commands
from .utils import checks
import discord, asyncio, aiohttp

class Foaas():
    """Tells someone/something to fuck off."""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def fetch(self, *mode):
        for arg in mode:
            params += arg + '/'
        async with self.session.get('http://foaas.com/', params=params) as data:
            req = await data.json()
        return req

    @commands.group(pass_context=True)
    @checks.is_owner()
    async def fuckoff(self, ctx):
        """Displays a fuck off message of your choosing."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('You need a mode. Type ?help fuckoff for more help.')

    @fuckoff.command(pass_context=True)
    @checks.is_owner()
    async def anyway(self, ctx, company:str):
        await self.bot.say(company + '\n' + ctx.message.author)
        fetch('anyway', company, ctx.message.author)


def setup(bot):
    bot.add_cog(Foaas(bot))
