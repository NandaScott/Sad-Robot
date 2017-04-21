from discord.ext import commands
from .utils import checks
import discord
import sqlite3, re
import os.path
import traceback

class TagAlias():
    def __init__(self, bot):
        self.bot = bot

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
        """Let's you reference images using keyword tags."""
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            try:
                cursor.execute('''select url from tag where tag=? and author=? and server_id=?''', (message.lower(), ctx.message.author.id, ctx.message.server.id))
            except Exception:
                db.rollback()
                db.close()
                await self.bot.say("You cannot access that tag.")
                return
            tag = cursor.fetchone()
            msg = discord.Embed(color=discord.Color(0x7ddd6e))
            msg.set_image(url=tag[0])
            await self.bot.say(embed=msg)
            cursor.execute('''update tag set number_of_uses = number_of_uses + 1 where tag=? ''', (message.lower(),))
            db.commit()
        except Exception:
            db.rollback()
            await self.bot.say(traceback.format_exc())
            return
        finally:
            db.close()

    @tag.command(pass_context=True, aliases=['add'])
    @checks.is_owner()
    async def make(self, ctx, *, message : str):
        """Used to add an image to the tag."""
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

    @tag.command(pass_context=True)
    @checks.is_owner()
    async def search(self, ctx):
        """Null"""
        pass

    @tag.command(pass_context=True)
    @checks.is_owner()
    async def raw(self, ctx, *, message:str):
        """Returns the raw tag url that you own."""
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            try:
                cursor.execute('''select url from tag where tag=? and author=? and server_id=?''', (message.lower(), ctx.message.author.id, ctx.message.server.id))
            except Exception:
                db.rollback()
                db.close()
                await self.bot.say("You cannot access that tag.")
                return
            tag = cursor.fetchone()
            await self.bot.say(tag[0])
            cursor.execute('''update tag set number_of_uses = number_of_uses + 1 where tag = '%s' ''' % message.lower())
            db.commit()
        except Exception:
            db.rollback()
            await self.bot.say(traceback.format_exc())
            return
        finally:
            db.close()

    @tag.group(pass_context=True)
    @checks.is_owner()
    async def edit(self, *, command:str):
        """Broken."""
        pass

    @edit.command(pass_context=True)
    @checks.is_owner()
    async def tag(self, ctx, *, message:str):
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            (tag, ntag) = re.match("(?P<tag>.*?) (?P<ntag>.*?)", message).groups()
            cursor.execute('''update tag set tag=? where tag=? and author=? and server_id=? ''', (ntag, tag, ctx.message.author.id, ctx.message.server.id))
            db.commit()
            await self.bot.say("Tag has been updated.")
        except Exception:
            db.rollback()
            await self.bot.say(traceback.format_exc())
            return
        finally:
            db.close()

    @edit.command(pass_context=True)
    @checks.is_owner()
    async def url(self, ctx, *, message:str):
        pass

    # @tag.command(pass_context=True)
    # @checks.is_owner()
    # async def info(self, ctx, *, tag:str):
    #     db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
    #     cursor = db.cursor()
    #     cursor.execute('''select * from tag where author=? and server_id=?''', (ctx.message.author.id, ctx.message.author.id))
    #     info = cursor.fetchall()
    #     msg = discord.Embed(color=discord.Color(0x7ddd6e))




def setup(bot):
    bot.add_cog(TagAlias(bot))
