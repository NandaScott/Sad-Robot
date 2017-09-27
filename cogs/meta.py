import discord, time
from discord.ext import commands

class Meta():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self):
        """Displays my source code."""
        await self.bot.say("https://github.com/NandaScott/Sad-Robot")

    @commands.command()
    async def playing(self, *, name:str):
        """Changes the game the bot is playing."""
        await self.bot.change_presence(game=discord.Game(name=name))

    @commands.command()
    async def ping(self):
        """Pings the bot."""
        startTimer = time.monotonic()
        await self.bot.say("**Pong!** \N{TABLE TENNIS PADDLE AND BALL}")
        endTimer = time.monotonic()
        result = endTimer - startTimer
        await self.bot.say("*Round trip time is {} seconds.*".format('%.3f' % result))

def setup(bot):
    bot.add_cog(Meta(bot))
