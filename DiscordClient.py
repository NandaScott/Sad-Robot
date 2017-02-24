import discord
import card


client = discord.Client()
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}... I guess...'.format(message)
        await client.send_message(message.channel, msg)

    #Card fetching section
    content = message.content
    fin = len(content)
    debut = content.find("[") + 1
    while debut > 0:
        # ss1 = content[ouvert: fin]
        fin = content.find("]", debut)
        requete = content[debut: fin]
        print("Request: " + requete)
        if len(requete) > 2:
            msg_list = card.card_fetch(requete)
            for msg in msg_list:
                await client.send_message(message.channel, msg)
        debut = content.find("[", fin) + 1

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('MjgzNzU1MjA4MDUwMjEyODY0.C5DCLA.eBJ1lGI1v96RUj7iq82M26gL6JM') #gitignore
