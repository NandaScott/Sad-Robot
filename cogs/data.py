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

    @commands.command
    async def tag(self):
        pass


def setup(bot):
    bot.add_cog(data(bot))
