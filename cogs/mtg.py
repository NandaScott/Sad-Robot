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
        if ctx.invoked_subcommand is None:
            startTimer = time.monotonic()
            card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
            endTimer = time.monotonic()
            f = endTimer - startTimer

            if card['object'] == "error":
                await self.bot.say(card['details'])
                return

            message = discord.Embed(
                title="**{}**".format(card['name']),
                url=card['scryfall_uri'],
                color=discord.Color(0x1b6f9),
                description=""
            )

            message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
            message.set_image(url=card['image_uri'])
            await self.bot.say(embed=message)

    @mtg.command(aliases=['p'])
    async def price(self, *, cardname : str):
        """Fetches the price of the card."""
        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
        endTimer = time.monotonic()
        f = endTimer - startTimer

        if card['object'] == "error":
            await self.bot.say(card['details'])
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )

        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_thumbnail(url=card['image_uri'])

        fields = ['usd', 'eur', 'tix']
        for currency in fields:
            try:
                message.add_field(name=currency.upper(), value='{:,.2f}'.format(float(card[currency])))
            except KeyError:
                pass

        await self.bot.say(embed=message)

    @mtg.command(aliases=['o'])
    async def oracle(self, *, cardname : str):
        """Fetches oracle text of the card."""
        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
        endTimer = time.monotonic()
        f = endTimer - startTimer


        if card['object'] == "error":
            await self.bot.say(card['details'])
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )
        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_thumbnail(url=card['image_uri'])

        if card['cmc'] != "0.0":
                message.title +=" "+card['mana_cost']
        message.description += card['type_line']+"\n"+card['oracle_text']
        if "Creature" in card['type_line']:
            message.description += "\n \n"+card['power']+"/"+card['toughness']
        if "Planeswalker" in card['type_line']:
            message.description += "\n Starting loyalty: "+card['loyalty']

        await self.bot.say(embed=message)

    @mtg.command(alias=['l', 'legality'])
    async def legal(self, *, cardname : str):
        """Fetches the formats the card is legal in."""
        startTimer = time.monoto, nic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname})
        endTimer = time.monotonic()
        f = endTimer - startTimer

        if card['object'] == "error":
            await self.bot.say(card['details'])
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )
        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_thumbnail(url=card['image_uri'])

        for key, value in card['legalities'].items():
                message.add_field(name=key[:1].upper()+key[1:], value=re.sub('_', " ", value[:1].upper()+value[1:]), inline=True)

        await self.bot.say(embed=message)

    @mtg.command(name='set', pass_context=True)
    async def edition(self, ctx, *args : str):
        """Fetches the image of a certain set. Requires the 3 letter code.

        Usage: ?mtg set <cardname> <setcode>"""
        cardname = args[:-2]
        setcode = args[-1]
        startTimer = time.monotonic()
        card = await self.getRequest(url='http://api.scryfall.com/cards/named?', params={'fuzzy':cardname, 'set':setcode})
        endTimer = time.monotonic()
        f = endTimer - startTimer

        if card['object'] == "error":
            await self.bot.say(card['details'])
            return

        message = discord.Embed(
            title="**{}**".format(card['name']),
            url=card['scryfall_uri'],
            color=discord.Color(0x1b6f9),
            description=""
        )

        message.set_footer(text="Fetch took: {} seconds.".format('%.3f' % f))
        message.set_image(url=card['image_uri'])
        await self.bot.say(embed=message)

def setup(bot):
    bot.add_cog(Mtg(bot))
