import discord
import re
from discord.ext import commands


class Fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def piglatin(self, *, words : str):
        """Will translate the following sentence into Pig Latin."""
        dictionary = {
            "suffix":"ay",
            "punctuation":'.,!?;',
            "vowels":'aeiuo',
            "digraphs":['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp',
                        'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr'],
            "trigraphs":['sch', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr']
        }
        message = ""
        sentence = re.findall(r"[\w']+|[.,!?;]", words)
        for word in sentence:

            firstChunk = word[0]
            restOfTheWord = word[1:]

            if word[:3].lower() in dictionary['trigraphs']:
                firstChunk = word[:3]
                restOfTheWord = word[3:]
            elif word[:2].lower() in dictionary['digraphs']:
                firstChunk = word[:2]
                restOfTheWord = word[2:]

            if word[0] == word[0].upper():
                try:
                    restOfTheWord = restOfTheWord[0].upper() + restOfTheWord[1:]
                    firstChunk = firstChunk.lower()
                except IndexError:
                    pass

            if firstChunk.lower() in dictionary['vowels']:
                message += " " + restOfTheWord + firstChunk + 'w' + dictionary['suffix']
            elif firstChunk in dictionary['punctuation']:
                message += firstChunk
            elif isinstance(int(word), int):
                message += word
            else:
                message += " " + restOfTheWord + firstChunk + dictionary['suffix']

        await self.bot.say(message)

    @commands.command()
    async def lmgtfy(self, *, query : str):
        """Let me google that for you."""
        search = "+".join(re.findall(r"[\w']+|[.,!?;]", query))
        newMessage = discord.Embed(title="Google", url='http://lmgtfy.com/?q={}'.format(search), color=discord.Color(0x1b6f9))
        await self.bot.say(embed=newMessage)


    @commands.command()
    async def memetext(self, *, message:str):
        """Responds with your message, but with more meme added."""
        newMessage = ""
        for character in list(message):
            if character == " ":
                newMessage += "  "
            elif isinstance(int(character), int):
                await self.bot.say("Unexpectedly, numbers aren't an emoji. Can't meme this text yo.")
                return
            else:
                newMessage += ":regional_indicator_%s:" % character
        await self.bot.say(newMessage)

def setup(bot):
    bot.add_cog(Fun(bot))
