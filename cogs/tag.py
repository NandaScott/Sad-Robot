from discord.ext import commands
from .utils import checks
import discord, sqlite3, re, os.path, traceback

class Tag():
    """These are the commands that are related to the tag function."""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, invoke_without_command=True)
    async def tag(self, ctx, *, message : str):
        """Let's you reference images using keyword tags."""
        if message is None:
            await self.bot.say("I need a tag to search with.")
            return
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
    async def make(self, ctx, *, message : str):
        """Used to add an image to the tag."""
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
        cursor = db.cursor()
        try:
            (tag, url) = re.match("(?P<tag>.*?) (?P<url>[^ ]*)$", message).groups()
            author = ctx.message.author.id
            server_id = ctx.message.server.id
            cursor.execute('''insert into tag(tag, url, author, server_id, number_of_uses) values(?,?,?,?,?)''', (tag, url, author, server_id, 0))
            await self.bot.say('Tag successfully inserted.')
            db.commit()
        except Exception:
            db.rollback()
            await self.bot.say(traceback.format_exc())
            return
        finally:
            db.close()

    @tag.command(pass_context=True)
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

    # @tag.command(pass_context=True)
    # @checks.is_owner()
    # async def info(self, ctx):
    #     db = sqlite3.connect(os.path.dirname(__file__) + "/lib/tags.db")
    #     cursor = db.cursor()
    #     cursor.execute('''select * from tag where author=? and server_id=?''', (ctx.message.author.id, ctx.message.server.id))
    #     info = cursor.fetchall()
    #     msg = discord.Embed(color=discord.Color(0x7ddd6e))
    #     await self.bot.say(info)



def setup(bot):
    bot.add_cog(Tag(bot))
