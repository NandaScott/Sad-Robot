import aiohttp
import discord
import json

async with aiohttp.ClientSession() as session:
    # async def card_fetch(session, cardname):
    # # response = requests.get('http://api.scryfall.com/cards/search', params={'q':cardname}).json()
    # # embed = discord.Embed(url=response['data'][0]['scryfall_uri'], color=discord.Color(0x1b6f9))
    # # embed.title = "**" + response['data'][0]['name'] + "** "
    # # if response['data'][0]['converted_mana_cost'] != "0.0":
    # #     embed.title += response['data'][0]['mana_cost']
    # # embed.description = response['data'][0]['type_line']
    # # if "Creature" in response['data'][0]['type_line']:
    # #     embed.description += " "+response['data'][0]['power']+"/"+response['data'][0]['toughness']+"\n"
    # # embed.description += " - *"+response['data'][0]['set'].upper()+"* \n"
    # # embed.description += response['data'][0]['oracle_text']+"\n"
    # # return embed
    #     pass


    async def cardimage_fetch(session, cardname):
        async with session.get('http://api.scryfall.com/cards/named?', params={'fuzzy':cardname}) as resp:
            return await resp.json()
    # response = requests.get('http://api.scryfall.com/cards/search', params={'q':cardname}).json()
    # msg = discord.Embed(url=response['data'][0]['scryfall_uri'], color=discord.Color(0x1b6f9))
    # msg.title = "**"+response['data'][0]['name']+"**"
    # msg.set_image(url=response['data'][0]['image_uri'])
    # return msg
