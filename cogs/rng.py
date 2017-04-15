import random
import re
import json
import aiohttp, discord
from discord.ext import commands

class RNG():
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

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
        async with open('/lib/temp_data.json') as data_file:
            data = json.load(data_file)
            heros = random.sample(data['heros'], 1)
            await self.bot.say(heros)


    @commands.command()
    async def lenny(self):
        """Displays a random lenny face."""
        lenny = random.choice([
            "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)",
            "( ͡o ͜ʖ ͡o)", "( ͡° ͜ʖ ͡ -)", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "(ง ͠° ͟ل͜ ͡°)ง",
            "ヽ༼ຈل͜ຈ༽ﾉ"
        ])
        await self.bot.say(lenny)

    @commands.command()
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
        async with self.session.get('http://random.cat/meow') as r:
            js = await r.json()
        msg = discord.Embed(color=discord.Color(0x8e75ff))
        msg.set_image(url=js['file'])
        await self.bot.say(embed=msg)


def setup(bot):
    bot.add_cog(RNG(bot))
