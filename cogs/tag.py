from discord.ext import commands
from .utils import checks
import discord
import sqlite3, re
import os.path

class tag():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_owner()
    async def db(self, *, command: str):
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            cursor.execute('''%s''' % command.lower())
            db.commit()
        except Exception as e:
            db.rollback()
            await self.bot.say(str(e))
            return
        finally:
            db.close()

    @commands.command()
    async def tag(self, *, message : str):
        """Let's you reference images or quotes using keyword tags.

        Syntax: ?tag <image tag>
        Can only fetch if you spelled the tag correctly.
        """
        try:
            db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
            cursor = db.cursor()
            cursor.execute('''select url from tag where tag = '%s' ''' % message.lower())
            tag = cursor.fetchone()
            msg = discord.Embed(color=discord.Color(0x7ddd6e))
            msg.set_image(url=tag[0])
            await self.bot.say(embed=msg)
            db.close()
        except Exception as e:
            await self.bot.say(str(e))
            return

    @commands.command()
    async def make(self, *, message : str):
        try:
            args = re.split(', ', message)
            tag = str(args[0])
            url = str(args[1])
            db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
            cursor = db.cursor()
            cursor.execute('''insert into tag(tag, url) values(?,?) ''', (tag, url))
            await self.bot.say('Tag successfully inserted.')
            db.commit()
        except Exception as e:
            db.rollback()
            await self.bot.say(str(e))
            return
        finally:
            db.close()


def setup(bot):
    bot.add_cog(tag(bot))
