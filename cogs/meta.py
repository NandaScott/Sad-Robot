import discord
from discord.ext import commands

class meta():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self):
        """
        Displays my source code.
        """
        source_url = "https://github.com/NandaScott/Sad-Robot"
        await self.bot.say(source_url)

def setup(bot):
    bot.add_cog(meta(bot))
