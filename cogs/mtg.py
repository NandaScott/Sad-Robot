import asyncio, aiohttp, json
import discord
import argparse, shlex
import re, time
import random
from discord.ext import commands
from .utils import checks

class Arguments(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)

class Mtg():
    def __init__(self, bot):
        self.bot = bot
        loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=loop)

    async def get_json(self, url, **kwargs):
        async with self.session.get(url, **kwargs) as response:
            return await response.read()

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
        start = time.time()
        parser = Arguments(add_help=False, allow_abbrev=False)
        parser.add_argument('cardname', nargs='+')
        parser.add_argument('-p', '--price', action='store_true')
        parser.add_argument('-o', '--oracle', action='store_true')
        parser.add_argument('-l', '--legality', action='store_true')
        parser.add_argument('-s', '--set', action='store', nargs=1)

        try:
            args = parser.parse_args(shlex.split(message))
        except Exception as e:
            await self.bot.say(str(e))
            return

        data = await self.get_json(url='http://api.scryfall.com/cards/named?', params={'fuzzy': args.cardname, 'e:': args.set})
        card = json.loads(data.decode('utf-8'))

        if card['object'] == 'error':
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
            price = []
            try:
                if card['usd']:
                    price.append("**USD**: "+ '${:,.2f}'.format(float(card['usd'])))
            except:
                pass
            try:
                if card['eur']:
                    price.append(u"\u2022"+" **EUR**: "+'€{:,.2f}'.format(float(card['eur'])))
            except:
                pass
            try:
                if card['tix']:
                    price.append(u"\u2022"+" **TIX**: "+'{:,.2f}'.format(float(card['tix'])))
            except:
                pass
            if price == None:
                msg.description += "Sorry, the price for this edition aren't available yet."
            else:
                msg.description += "\n \n"+" ".join(price)


        if args.legality:
            legal = []
            illegal = []
            banned = []
            for key, value in card['legalities'].items():
                if value == "restricted":
                    msg.description += "**Restricted In**: "+key[:1].upper()+key[1:]
                if value == "legal":
                    legal.append(key[:1].upper()+key[1:])
                if value == "not_legal":
                    illegal.append(key[:1].upper()+key[1:])
                if value == "banned":
                    banned.append(key[:1].upper()+key[1:])

            if not illegal and not banned:
                msg.description +="\n \n **Legal In**: "+u" \u2022 ".join(legal)
            else:
                msg.description += "\n **Not Legal In**: "+u" \u2022 ".join(illegal)+"\n **Banned In**: "+u" \u2022 ".join(banned)

        end = time.time()
        f = end - start
        print("Card fetch took: "+str('%.3f'%f)+" seconds to complete.")
        await self.bot.say(embed=msg)


    # @commands.command()
    # @checks.is_owner()
    # async def spoilers(self, *, set_name : str):
    #     while True:
    #         data = await self.get_json(url='http://api.scryfall.com/cards/search?', params={'q':'++e:akh', 'order':'spoiler'})
    #         decoded_json = json.loads(data.decode('utf-8'))
    #         count = decoded_json['total_cards']
    #         msg = discord.Embed(color=discord.Color(0xa8ff6b))
    #         msg.title = "**New Spoilers**"
    #         if count > decoded_json['total_cards']:
    #             for card in range(count, decoded_json['total_cards']):
    #                 msg.description += "["+decoded_json['data'][incr]['name']+"]("+decoded_json['data'][incr]['scryfall_uri']+")"
    #                 incr += 1
    #         time.sleep(600)
    #     await self.bot.say(embed=msg)




def setup(bot):
    bot.add_cog(Mtg(bot))
