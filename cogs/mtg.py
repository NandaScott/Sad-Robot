import asyncio, aiohttp, json
import discord, re, time
from discord.ext import commands
from .utils import checks

class Mtg():
    def __init__(self, bot):
        self.bot = bot

    async def getRequest(self, url, **kwargs):
        async with self.bot.aiohttp_session.get(url, **kwargs) as response:
            return await response.json()

    @commands.group(aliases=['MTG', 'Mtg'], pass_context=True, invoke_without_command=True)
    async def mtg(self, ctx, *, cardname : str):
        """
        Fetches for a card.

        The bot can correct spelling errors, but will also fetch Un-set cards so be careful.
        """

        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
        endTimer = time.monotonic()
        f = endTimer - startTimer

        if card['object'] == "error":
            await self.bot.say(re.sub(r'\(|\'|,|\)+', '', card['details']))
            return

        if card['card_faces']:
            for entry in card['card_faces']:
                message = discord.Embed(
                    title="**{}**".format(entry['name']),
                    url=card['scryfall_uri'],
                    color=discord.Color(0x1b6f9)
                )
                message.set_image(url=entry['image_uris']['normal'])
                message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
                await self.bot.say(embed=message)
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )

        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_image(url=card['image_uris']['normal'])
        await self.bot.say(embed=message)

    @mtg.command(aliases=['-p', '--price'])
    async def price(self, *, cardname : str):
        """Fetches the price of the card."""
        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
        endTimer = time.monotonic()
        f = endTimer - startTimer

        if card['object'] == "error":
            await self.bot.say(re.sub(r'\(|\'|,|\)+', '', card['details']))
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )

        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_thumbnail(url=card['image_uris']['normal'])

        fields = ['usd', 'eur', 'tix']
        for currency in fields:
            try:
                message.add_field(name=currency.upper(), value='{:,.2f}'.format(float(card[currency])))
            except KeyError:
                pass

        await self.bot.say(embed=message)

    @mtg.command(aliases=['-o', '--oracle'])
    async def oracle(self, *, cardname : str):
        """Fetches oracle text of the card."""
        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
        endTimer = time.monotonic()
        f = endTimer - startTimer


        if card['object'] == "error":
            await self.bot.say(re.sub(r'\(|\'|,|\)+', '', card['details']))
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )
        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))

        if card['card_faces']:
            card_images = None
            for entry in card['card_faces']:
                message.description += "\n=========\n"
                if card['cmc'] != "0.0":
                    message.description += "**"+entry['name']+"** "+entry['mana_cost']+"\n"
                message.description += entry['type_line']+"\n"+entry['oracle_text']
                if "Creature" in entry['type_line']:
                    message.description += "\n \n"+entry['power']+"/"+entry['toughness']
                if "Planeswalker" in entry['type_line']:
                    message.description += "\n Starting loyalty: "+entry['loyalty']
            await self.bot.say(embed=message)
            return

        message.set_thumbnail(url=card['image_uris']['normal'])

        if card['cmc'] != "0.0":
                message.title +=" "+card['mana_cost']
        message.description += card['type_line']+"\n"+card['oracle_text']
        if "Creature" in card['type_line']:
            message.description += "\n \n"+card['power']+"/"+card['toughness']
        if "Planeswalker" in card['type_line']:
            message.description += "\n Starting loyalty: "+card['loyalty']

        await self.bot.say(embed=message)

    @mtg.command(alias=['-l', '--legality'])
    async def legal(self, *, cardname : str):
        """Fetches the formats the card is legal in."""
        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
        endTimer = time.monotonic()
        f = endTimer - startTimer

        if card['object'] == "error":
            await self.bot.say(re.sub(r'\(|\'|,|\)+', '', card['details']))
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )
        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_thumbnail(url=card['image_uris']['normal'])

        for key, value in card['legalities'].items():

                if value == "banned":
                    symbol = ":no_entry:"
                if value == "not_legal":
                    symbol = ":x:"
                if value == "legal":
                    symbol = ":white_check_mark:"

                message.add_field(
                name=key[:1].upper()+key[1:],
                value="{} {}".format(
                    re.sub('_', " ", value[:1].upper()+value[1:]), symbol)
                )

        await self.bot.say(embed=message)

    @mtg.command(name='set', pass_context=True)
    async def edition(self, ctx, *args : str):
        """Fetches the image of a certain set. Requires the 3 letter code.

        Usage: ?mtg set <cardname> <setcode>"""
        cardname = args[0:len(args)-1]
        setcode = args[-1]
        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname, 'set':setcode})
        endTimer = time.monotonic()
        f = endTimer - startTimer

        if card['object'] == "error":
            await self.bot.say(re.sub(r'\(|\'|,|\)+', '', card['details']))
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )

        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_image(url=card['image_uris']['normal'])
        await self.bot.say(embed=message)

    @mtg.command(pass_context=True)
    async def random(self, ctx):
        """Fetches a random card."""
        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/random')
        endTimer = time.monotonic()
        f = endTimer - startTimer

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )

        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_image(url=card['image_uris']['normal'])
        await self.bot.say(embed=message)



def setup(bot):
    bot.add_cog(Mtg(bot))
