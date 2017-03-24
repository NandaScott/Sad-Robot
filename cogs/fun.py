import discord
import re
from discord.ext import commands


class Fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def piglatin(self, *, words : str):
        pyg = 'ay'
        vowels = ['a', 'e', 'i', 'o', 'u']
        digraphs = ['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp',
        'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr']
        trigraphs = ['sch', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr']
        msg = ""
        sentence = re.split(" ", words)
        for word in sentence:
            #Checks for Digraphs and Trigraphs
            if word[0:2].lower() in digraphs:
                first = word[0:2]
                pygify = word[2:]
            elif word[0:3].lower() in trigraphs:
                first = word[0:3]
                pygify = word[3:]
            else:
                pygify = word[1:]
                first = word[0]
            #Replaces capitalization
            if first[0] == first[0].upper():
                try:
                    pygify = pygify[0].upper() + pygify[1:]
                    first = first.lower()
                except IndexError:
                    pass
                    # Checks for vowels at the beginning of a word
            if first in vowels:
                stitch = pygify + first + 'w' + pyg
                msg += stitch + " "
            else:
                stitch = pygify + first + pyg
                msg += stitch + " "

        await self.bot.say(msg)




def setup(bot):
    bot.add_cog(Fun(bot))
