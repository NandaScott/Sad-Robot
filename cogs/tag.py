from discord.ext import commands
from .utils import checks
from urllib.parse import urlparse
import discord
import sqlite3, re
import os.path
import traceback

class Tag():
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

    @commands.group(pass_context=True, invoke_without_command=True)
    @checks.is_owner()
    async def tag(self, ctx, *, message : str):
        """Let's you reference images using keyword tags.
        """
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
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

    @tag.command(pass_context=True)
    @checks.is_owner()
    async def make(self, ctx, *, message : str):
        """Used to add an image to the tag.

        Syntax: ?make <tag> <url>
        Only accepts valid urls.
        """
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            (tag, url) = re.match("(?P<tag>.*?) (?P<url>[^ ]*)$", message).groups()
            author = ctx.message.author.id
            server_id = ctx.message.server.id
            cursor.execute('''insert into tag(tag, url, author, server_id) values(?,?,?,?)''', (tag, url, author, server_id))
            await self.bot.say('Tag successfully inserted.')
            db.commit()
        except Exception:
            db.rollback()
            await self.bot.say(traceback.format_exc())
            return
        finally:
            db.close()


def setup(bot):
    bot.add_cog(Tag(bot))
