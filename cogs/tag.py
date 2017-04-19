from discord.ext import commands
from .utils import checks
from urllib.parse import urlparse
import discord
import sqlite3, re
import os.path
import traceback

class tag():
    def __init__(self, bot):
        self.bot = bot

    # async def validate_url(arg):
    #     parsed_url = urlparse(arg)
    #     e = bool(parsed_url.scheme)
    #     return e

    @commands.command(hidden=True)
    @checks.is_owner()
    async def db(self, *, command: str):
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            cursor.execute('''%s''' % command.lower())
            await self.bot.say('Command successful.')
            db.commit()
        except Exception as e:
            db.rollback()
            await self.bot.say(str(e))
            return
        finally:
            db.close()

    @commands.command()
    async def tag(self, *, message : str):
        """Let's you reference images using keyword tags.

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
        except Exception:
            db.rollback()
            await self.bot.say('Can\'t be found. Double check your spelling.')
            return
        finally:
            db.close()

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def make(self, ctx):
        """Used to add an image to the tag.

        Syntax: ?make <tag>, <url>
        Only accepts valid urls.
        """
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            message = ctx.message.content
            (_, tag, url) = re.split(' ', message)
            author = ctx.message.author.id
            cursor.execute('''insert into tag(tag, url, author) values(?,?,?)''', (tag, url, author))
            await self.bot.say('Tag successfully inserted.')
            db.commit()
        except Exception:
            db.rollback()
            await self.bot.say(traceback.format_exc())
            return
        finally:
            db.close()


def setup(bot):
    bot.add_cog(tag(bot))
