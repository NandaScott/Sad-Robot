import discord
from discord.ext import commands

class Meta():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self):
        """
        Displays my source code.
        """
        source_url = "https://github.com/NandaScott/Sad-Robot"
        await self.bot.say(source_url)

    @commands.command()
    async def playing(self, *, name:str):
        """Changes the game the bot is playing."""
        await self.bot.change_presence(game=discord.Game(name=name))

def setup(bot):
    bot.add_cog(Meta(bot))
