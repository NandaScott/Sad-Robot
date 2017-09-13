import discord
import re
from discord.ext import commands


class Fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def piglatin(self, *, words : str):
        """Will translate the following sentence into Pig Latin."""
        pyg = 'ay'
        punc = [".",",","!","?",";"]
        vowels = ['a', 'e', 'i', 'o', 'u']
        digraphs = ['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp',
        'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr']
        trigraphs = ['sch', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr']
        msg = ""
        sentence = re.findall(r"[\w']+|[.,!?;]", words)
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
                msg += " " + stitch
            elif first in punc:
                msg += first
            else:
                stitch = pygify + first + pyg
                msg += " " + stitch

        await self.bot.say(msg)

    @commands.command()
    async def lmgtfy(self, *, words : str):
        """Let me google that for you."""
        search = "+".join(re.findall(r"[\w']+|[.,!?;]", words))
        url = 'http://lmgtfy.com/?q=%s' % search
        msg = discord.Embed(url=url, color=discord.Color(0x1b6f9))
        msg.title = "Google"
        await self.bot.say(embed=msg)


    @commands.command()
    async def memetext(self, *, message:str):
        msg = ""
        for character in list(message):
            if character == " ":
                msg += "  "
            else:
                msg += ":regional_indicator_%s:" % character
        await self.bot.say(msg)

    # Currently under construction
    # @bot.event()
    # async def on_message(self, ctx):
    #     if ctx.message.content == "You can't" or "you can't"
    #         i = True
    #         ret = ""
    #         for char in ctx.message.content:
    #             if i:
    #                 ret += char.upper()
    #             else:
    #                 ret += char.lower()
    #             if char != ' ':
    #                 i = not i
    #         await self.bot.process_commands(ret)


def setup(bot):
    bot.add_cog(Fun(bot))
