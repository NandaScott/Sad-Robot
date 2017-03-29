import asyncio, aiohttp, json
import discord
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

    async def get_json(self, url, **kwargs):
        async with self.session.get(url, **kwargs) as response:
            # print(response.status)
            assert response.status == 200
            return await response.read()

    @commands.command()
    async def mtg(self, *, message : str):
        """
        Fetches MTG cards.

        ?mtg "<cardname>" <argument(s)>

        positional arguments:
        "<cardname>"    You must have a card to fetch for. The bot can correct spelling errors,
                        but will also fetch Un-set cards so be careful. You also must have quotation marks.

        optional arguments:
        -p, --price     Will fetch the price of the called card.
        -o, --oracle    Will fetch the most recent oracle text of the called card.
        -l, --legality  Will fetch the legalities of the card.
        """

        parser = Arguments(add_help=False, allow_abbrev=False)
        parser.add_argument('cardname', nargs="+")
        parser.add_argument('-p', '--price', action='store_true')
        parser.add_argument('-o', '--oracle', action='store_true')
        parser.add_argument('-l', '--legality', action='store_true')

        try:
            args = parser.parse_args(shlex.split(message))
        except Exception as e:
            await self.bot.say(str(e))
            return

        data = await self.get_json(url='http://api.scryfall.com/cards/named?', params={'fuzzy': args.cardname})

        card = json.loads(data.decode('utf-8'))
        msg = discord.Embed(url=card['scryfall_uri'], color=discord.Color(0x1b6f9))
        msg.title = "**" + card['name'] + "**"
        msg.description = ""

        if args.oracle is False and args.price is False and args.legality is False:
            msg.set_image(url=card['image_uri'])

        if args.oracle:
            msg.set_thumbnail(url=card['image_uri'])
            msg.title +=" "+card['mana_cost']
            msg.description += card['type_line']+"\n"+card['oracle_text']
            if "Creature" in card['type_line']:
                msg.description += "\n \n"+card['power']+"/"+card['toughness']

        if args.price:
            price = []
            if card['usd']:
                price.append("**USD**: "+ '${:,.2f}'.format(float(card['usd'])))
            if card['eur']:
                price.append(u"\u2022"+" **EUR**: "+'€{:,.2f}'.format(float(card['eur'])))
            if card['tix']:
                price.append(u"\u2022"+" **TIX**: "+'{:,.2f}'.format(float(card['tix'])))
            msg.description += "\n \n"+" ".join(price)
            msg.set_thumbnail(url=card['image_uri'])

        # This is spaghetti code but I couldn't iterate through it. Temp fix.
        if args.legality:
            legal_in = []
            not_legal = []
            restricted =[]
            legal_in.append('Standard') if card['legalities']['standard'] == "legal" else not_legal.append('Standard')
            legal_in.append('Frontier') if card['legalities']['frontier'] == "legal" else not_legal.append('Frontier')
            legal_in.append('Modern') if card['legalities']['modern'] == "legal" else not_legal.append('Modern')
            legal_in.append('Pauper') if card['legalities']['pauper'] == "legal" else not_legal.append('Pauper')
            legal_in.append('Legacy') if card['legalities']['legacy'] == "legal" else not_legal.append('Legacy')
            legal_in.append('Penny Dreadful') if card['legalities']['penny'] == "legal" else not_legal.append('Penny Dreadful')
            legal_in.append('Duel Comm.') if card['legalities']['duel'] == "legal" else not_legal.append('Duel Comm.')
            legal_in.append('Commander') if card['legalities']['commander'] == "legal" else not_legal.append('Commander')
            #Vintage is a special case since it's the only format with restrictions.
            if card['legalities']['vintage'] == 'restricted':
                restricted.append('Vintage')
            else:
                legal_in.append('Vintage') if card['legalities']['vintage'] == "legal" else not_legal.append('Vintage')
            msg.description +="\n \n"+"**Legal In**: "+u" \u2022 ".join(legal_in)+"\n **Not Legal In**: "+u" \u2022 ".join(not_legal)
            msg.description +="\n"+"**Restricted In**: "+"".join(restricted)
            msg.set_thumbnail(url=card['image_uri'])


        await self.bot.say(embed=msg)

def setup(bot):
    bot.add_cog(Mtg(bot))
