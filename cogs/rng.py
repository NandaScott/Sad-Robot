import random
import re
from discord.ext import commands

class RNG():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, dice : str):
        # Rolls a dice in NdN format.
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *, choices : str):
        await self.bot.say(random.choice(re.split(', ', choices)))

    @commands.command(description='For choosing a random overwatch hero.')
    async def rhero(self):
        heros=random.choice([
        'Genji. Embrace your inner weeb.',
        'Mccree. Reach for the sky!',
        'Pharah. JUSTICE RAINS FROM-AAAUGH!',
        'Reaper. Mom didn\'t hug me enough.',
        'Soldier:76. Call of Battlefield, Modern war games.',
        'Sombra. *Hacks you in spanish*',
        'Tracer. Cheers love! The cavelry\'s queer!',
        'Bastion. Beep Boop, fuck the red team.',
        'Hanzo. SAKE!',
        'Junkrat. For when you don\'t need to aim.',
        'Mei. Fuck you.',
        'Torbjörn. Cause we\'re on attack right?',
        'Widowmaker. You won\'t switch and you know it.',
        'D.va. :wink:',
        'Orisa. Neigh.',
        'Reinhardt. *Hanzo can you go Rein?*',
        'Roadhog. One man a-pork-calypse.',
        'Winston. DICKS OUT FOR HARAMBE XDDDDDD.',
        'Zarya. CREDIT TO TEAM.',
        'Ana. Grandma says it\'s naptime.',
        'Lucio. I\'m existing as best as I can.',
        'Mercy. Nice team wipe you had there.',
        'Symmetra. :musical_note: Tunak Tunak Tun Tunak Tunak Tun :musical_note:',
        'Zenyatta. Show everyone how many balls you have.'
        ])
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


def setup(bot):
    bot.add_cog(RNG(bot))
