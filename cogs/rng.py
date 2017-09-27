import random, re, json
import asyncio, aiohttp, discord
import os.path, sqlite3
from discord.ext import commands
from .utils import checks

class RNG():
    """For when you don't want bias."""
    def __init__(self, bot):
        self.bot = bot

    async def getRequest(self, url, **kwargs):
        async with self.bot.aiohttp_session.get(url, **kwargs) as response:
            return await response.json()

    @commands.command()
    async def roll(self, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command()
    async def choose(self, *, choices : str):
        """Chooses between multiple options."""
        try:
            await self.bot.say(random.choice(re.split(', | or ', choices)))
        except Exception:
            await self.bot.say('Format should be <choice1>, <choice2>. You can also <choice1> or <choice2>. ')
            return

    @commands.command()
    async def rhero(self):
        """For choosing a random Overwatch hero."""
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/overwatch.db")
        cursor = db.cursor()
        message = discord.Embed(color=discord.Color(0x8e75ff))
        try:
            cursor.execute('''select name from heros where name is not null order by random() limit 1''')
            message.title = cursor.fetchone()[0]
        except Exception as e:
            db.rollback()
            await self.bot.say(str(e))
        finally:
            await self.bot.say(embed=message)
            db.close()

    @commands.command(name='8ball')
    async def fortune(self):
        """Works like an 8ball. Ask it a question."""
        responses = random.choice([
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Nigga no."
        ])
        await self.bot.say(responses)

    @commands.command()
    async def cat(self):
        """Displays a random cat image

        You really need help with this one?
        """
        cat =  self.getRequest(url='http://random.cat/meow')
        message = discord.Embed(color=discord.Color(0x8e75ff))
        message.set_image(url=cat['file'])
        await self.bot.say(embed=message)

def setup(bot):
    bot.add_cog(RNG(bot))
