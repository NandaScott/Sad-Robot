import asyncio, aiohttp, json
import discord
import argparse, shlex
import re, time
import random
from discord.ext import commands
from .utils import checks, tools

class Arguments(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)

class Mtg():
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()


    @commands.command()
    async def mtg(self, *, message : str):
        """
        Fetches MTG cards.

        ?mtg <cardname> <argument(s)>

        positional arguments:
        <cardname>    You must have a card to fetch for. The bot can correct
                        spelling errors, but will also fetch Un-set cards so be
                        careful.

        optional arguments:
        -p, --price     Will fetch the price of the called card.
        -o, --oracle    Will fetch the most recent oracle text of the card.
        -l, --legality  Will fetch the legalities of the card.
        """

        # start = time.time()
        parser = Arguments(add_help=False, allow_abbrev=False)
        parser.add_argument('cardname', nargs='+')
        parser.add_argument('-p', '--price', action='store_true')
        parser.add_argument('-o', '--oracle', action='store_true')
        parser.add_argument('-l', '--legality', action='store_true')
        parser.add_argument('-s', '--set', action='store', nargs=1)

        try:
            args = parser.parse_args(shlex.split(re.sub(r"\'", "", message)))
        except Exception as e:
            await self.bot.say(str(e))
            return

        async with self.session.get('http://api.scryfall.com/cards/named?', params={'fuzzy': args.cardname, 'e:': args.set}) as data:
            card = await data.json()

        if card['object'] == 'error':
            # TO DO: refactor this
            # e = tools.stripper("\[\'|\'\]|\', \'", " ", card['details'])
            e = card['details']
            ne = re.sub(r'\[\'', '', e)
            ne = re.sub(r'\'\]', '', ne)
            ne = re.sub(r'\', \'', ' ', ne)
            await self.bot.say(ne)
            return

        msg = discord.Embed(url=card['scryfall_uri'], color=discord.Color(0x1b6f9))
        msg.title = "**" + card['name'] + "**"
        msg.description = ""

        if args.oracle is False and args.price is False and args.legality is False:
            msg.set_image(url=card['image_uri'])
        else:
            msg.set_thumbnail(url=card['image_uri'])

        if args.oracle:
            if card['converted_mana_cost'] != "0.0":
                msg.title +=" "+card['mana_cost']
            msg.description += card['type_line']+"\n"+card['oracle_text']
            if "Creature" in card['type_line']:
                msg.description += "\n \n"+card['power']+"/"+card['toughness']
            if "Planeswalker" in card['type_line']:
                msg.description += "\n Starting loyalty: "+card['loyalty']

        if args.price:
                try:
                    msg.add_field(name="USD", value='${:,.2f}'.format(float(card['usd'])))
                except KeyError:
                    pass

                try:
                    msg.add_field(name="EUR", value='€{:,.2f}'.format(float(card['eur'])))
                except KeyError:
                    pass

                try:
                    msg.add_field(name="TIX", value='{:,.2f}'.format(float(card['tix'])))
                except KeyError:
                    pass

        if args.legality:
            for key, value in card['legalities'].items():
                msg.add_field(name=key[:1].upper()+key[1:], value=re.sub('_', " ", value[:1].upper()+value[1:]), inline=True)

        # end = time.time()
        # f = end - start
        # print("Card fetch took: "+str('%.3f'%f)+" seconds to complete.")
        await self.bot.say(embed=msg)
    #===================
    #===================
    #This doesn't work yet. So will revisit at a later date.

    async def request(self, cardname):
        url = 'http://api.scryfall.com/cards/named?' + 'fuzzy=' + '+'.join(cardname)
        async with self.session.get(url) as data:
            card = await data.json()
            return await card

    @commands.group(hidden=True)
    @checks.is_owner()
    async def mtg2(self, *, cardname : str):
        """Fetches a magic card."""
        card = self.request(cardname)
        msg = discord.Embed(url=card['scryfall_uri'], color=discord.Color(0x1b6f9))
        msg.title = "**" + card['name'] + "**"
        msg.set_image(url=card['image_uri'])
        await self.bot.say(embed=msg)


    @mtg2.command(name='-p')
    @checks.is_owner()
    async def price(self):
        """ Fetches the price of the magic card """

        try:
            msg.add_field(name="USD", value='${:,.2f}'.format(float(card['usd'])))
        except KeyError:
            pass

        try:
            msg.add_field(name="EUR", value='€{:,.2f}'.format(float(card['eur'])))
        except KeyError:
            pass

        try:
            msg.add_field(name="TIX", value='{:,.2f}'.format(float(card['tix'])))
        except KeyError:
            pass



def setup(bot):
    bot.add_cog(Mtg(bot))
