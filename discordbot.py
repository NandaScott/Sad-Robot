import card
from secret import token
from discord.ext import commands

bot = commands.Bot(command_prefix="?")

@bot.command(pass_context=True)
async def mtg(message : str, ctx):
    print("Requesting card: " + ctx)
    msg = card.cardimage_fetch(ctx)
    await bot.say(embed=msg)

#
# @bot.event
# async def on_message(message):
#     # we do not want the bot to reply to itself
#     if message.author == bot.user:
#         return
#
#     if message.content.startswith('!hello'):
#         msg = 'Hello {0.author.mention}... I guess...'.format(message)
#         await bot.send_message(message.channel, msg)

    #Card fetching section
    # content = message.content
    # fin = len(content)
    # grab = content.find("[")
    # debut = 1
    # while debut > 0:
    #     # ss1 = content[ouvert: fin]
    #     fin = content.find("]", grab)
    #     requete = content[grab: fin]
    #     print("Request: " + requete)
    #     if "#" in requete:
    #         embed = card.card_fetch(requete)
    #         await bot.send_message(message.channel, embed=embed)
    #     else:
    #         embed = card.cardimage_fetch(requete)
    #         await bot.send_message(message.channel, embed=embed)
    #
    #     grab = content.find("[", fin)
    #     debut=1

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(token)
