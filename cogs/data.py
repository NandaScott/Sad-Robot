from discord.ext import commands
from .utils import checks
import discord
import sqlite3
import os.path

class data():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_owner()
    async def db(self):

        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            cursor.execute('''
                create table tag(id integer primary key, url string, tag string)
                ''')
        except Exception as e:
            await self.bot.say(str(e))
            return

        db.commit()
        db.close()

    @commands.command()
    async def tag(self, *, message : str):
            """Let's you reference images or quotes using keyword tags."""
        try:
            db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
            cursor = db.cursor()
            cursor.execute('''select url from tag where tag = '%s' ''' % message.lower())
            tag = cursor.fetchone()
            msg = discord.Embed(color=discord.Color(0x1b6f9))
            msg.set_image(url=tag[0])
            await self.bot.say(embed=msg)
            db.close()
        except Exception as e:
            await self.bot.say(str(e))
            return

def setup(bot):
    bot.add_cog(data(bot))
