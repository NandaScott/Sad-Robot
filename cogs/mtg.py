import asyncio, aiohttp, json
import discord
import re
import argparse, shlex
from discord.ext import commands

class Arguments(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)

class Mtg():
    def __init__(self, bot):
        self.bot = bot
        loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=loop)

    @commands.command()
    async def mtg(self, *, message : str):

        parser = Arguments(add_help=False, allow_abbrev=False)
        parser.add_argument('-p', '--price')
        parser.add_argument('-o', '--oracle')
        parser.add_argument('-l', '--legality')
        parser.add_argument('-b', '--buy')
        parser.add_argument('-f', '--fuzzy')

        try:
            args = parser.parse_args(shlex.split(message))
        except Exception as e:
            await self.bot.say(str(e))
            return

        async def get_json(self, url, **kwargs):
            async with self.session.get(url, **kwargs) as response:
                assert response.status == 200
                return await response.read()

        cardname = "+".join(re.findall(r"[\w']+|[.,!?;]", message))

        if args.fuzzy:
            data = await self.get_json(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
        else:
            data = await self.get_json(url='http://api.scryfall.com/cards/search', params={'q': cardname})

        card = json.loads(data.decode('utf-8'))
        msg = discord.Embed(url=card['scryfall_uri'], color=discord.Color(0x1b6f9))

        if args is not None:
            msg.set_thumbnail(url=card['image_uri'])
        else:
            msg.set_image(url=card['image_uri'])
        msg.title = "**" + card['name'] + "**"

        if args.price:
            price = []
            if card['usd']:
                price.append("**USD**: "+'${:,.2f}'.format(card['usd']))
            elif card['eur']:
                price.append("**EUR**: "+'€{:,.2f}'.format(card['eur']))
            elif card['tix']:
                price.append("**TIX**: "+'{:,.2f}'.format(card['tix']))
            " ".join(price)
            msg.set_description(description=price)

        if args.oracle:
            msg.set_description(description=card['oracle_text'])

        if args.legality:
            legal_in = []
            not_legal = []
            for k, v in card['legalities']:
                if v == "legal":
                    legal_in.append(v)
                else:
                    not_legal.append(v)
            msg.add_field(name="Legal", value=legal_in)
            msg.add_field(name="Not Legal", value=not_legal)

        if args.buy:
            for k, v in card['pruchase_uris']:
                msg.set_description(description="["+k+"]("+v+")")

        await self.bot.say(embed=msg)
        # try:
        #     cardname = "+".join(re.findall(r"[\w']+|[.,!?;]", ctx))
        #     data = await self.get_json(url='http://api.scryfall.com/cards/named?', params={'fuzzy': cardname})
        #     card = json.loads(data.decode('utf-8'))
        #     msg = discord.Embed(url=card['scryfall_uri'], color=discord.Color(0x1b6f9))
        #     msg.set_image(url=card['image_uri'])
        #     msg.title = "**" + card['name'] + "**"
        #     await self.bot.say(embed=msg)
        # except Exception:
        #     await self.bot.say("Sorry, couldn't find that card. Check your spelling or syntax.")
        #     return

def setup(bot):
    bot.add_cog(Mtg(bot))
