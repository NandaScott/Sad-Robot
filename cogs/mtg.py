import asyncio, aiohttp, json
import discord
import argparse, shlex
import re, time, urllib
from discord.ext import commands
from .utils import checks, tools

class Arguments(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)

class Mtg():
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.bot.loop.create_task(self.spoilers())


    @commands.command(aliases=['MTG', 'Mtg'])
    async def mtg(self, *, cardname : str):
        """
        Fetches MTG cards.

        ?mtg <cardname> <argument(s)>

        positional arguments:
        <cardname>  You must have a card to fetch for.
                    The bot can correct spelling errors, but will also fetch
                    Un-set cards so be careful.

        optional arguments:
        -p, --price     Fetches the price of the card.
        -o, --oracle    Fetches the most recent oracle text of the card.
        -l, --legality  Fetches the legalities of the card.
        """

        start = time.time()
        parser = Arguments(add_help=False, allow_abbrev=False)
        parser.add_argument('cardname', nargs='*')
        parser.add_argument('-p', '--price', action='store_true')
        parser.add_argument('-o', '--oracle', action='store_true')
        parser.add_argument('-l', '--legality', action='store_true')
        # Will impliment when Scryfall makes a proper api for that
        # parser.add_argument('-s', '--set', action='store', nargs=1)

        try:
            args = parser.parse_args(shlex.split(re.sub(r"\'", "", cardname)))
        except Exception as e:
            await self.bot.say(str(e))
            return


        async with self.session.get('http://api.scryfall.com/cards/named?', params={'fuzzy':args.cardname}) as data:
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
        msg.description = None

        if args.oracle is False and args.price is False and args.legality is False:
            msg.set_image(url=card['image_uri'])
        else:
            msg.set_thumbnail(url=card['image_uri'])

        if args.oracle:
            if card['cmc'] != "0.0":
                msg.title +=" "+card['mana_cost']
            msg.description += card['type_line']+"\n"+card['oracle_text']
            if "Creature" in card['type_line']:
                msg.description += "\n \n"+card['power']+"/"+card['toughness']
            if "Planeswalker" in card['type_line']:
                msg.description += "\n Starting loyalty: "+card['loyalty']

        if args.price:
                fields = ['usd', 'eur', 'tix']
                for curr in fields:
                    try:
                        msg.add_field(name=curr.upper(), value='{:,.2f}'.format(float(card[curr])))
                    except KeyError:
                        pass

        if args.legality:
            for key, value in card['legalities'].items():
                msg.add_field(name=key[:1].upper()+key[1:], value=re.sub('_', " ", value[:1].upper()+value[1:]), inline=True)

        end = time.time()
        f = end - start
        msg.set_footer(text="Fetch took: "+str('%.3f'%f)+" seconds.")
        await self.bot.say(embed=msg)


    async def spoilers(self):
        set_code = '++e:xln'
        card_count = 0
        channel = discord.Object(id='352131916058591234')
        while not self.bot.is_closed:
            async with self.session.get('https://api.scryfall.com/cards/search?', params={'q':set_code, 'order':'spoiled'}) as data:
                card = await data.json()
            if card_count < card['total_cards']:
                msg = discord.Embed(color=discord.Color(0x1b6f9))
                msg.description = ""
                msg.title = '**New Spoilers**'
                c = 0
                for spoil in range(card_count, card['total_cards']):
                    msg.description += '['+card['data'][c]['name']+']('+card['data'][c]['scryfall_uri']+')' + '\n'
                    c += 1
                await self.bot.send_message(channel, embed=msg)
                card_count = card['total_cards']
            await asyncio.sleep(120)




def setup(bot):
    bot.add_cog(Mtg(bot))
