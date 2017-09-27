# This cog is brought to you by Rapptz on github.
# You can find it here: https://github.com/Rapptz/RoboDanny/blob/master/cogs/admin.py
import discord, inspect
import time, sqlite3, os.path
from collections import Counter
from discord.ext import commands
from .utils import checks

class Admin:
    """Admin-only commands that make the bot dynamic. Only for use for my master."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def db(self, *, table : str, command : str):
        """Executes SQL query manually."""
        db = sqlite3.connect(os.path.dirname(__file__) + "/lib/{}.db".format(table))
        cursor = db.cursor()
        try:
            cursor.execute('''?''', command.lower())
            await self.bot.say('Command successful.')
            db.commit()
        except Exception as e:
            db.rollback()
            await self.bot.say(str(e))
            return
        finally:
            db.close()

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def load(self, ctx, *, module : str):
        """Loads a module."""
        try:
            self.bot.load_extension("cogs.%s" % module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.add_reaction(ctx.message, '\N{OK HAND SIGN}')

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def unload(self, ctx, *, module : str):
        """Unloads a module."""
        try:
            self.bot.unload_extension("cogs.%s" % module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.add_reaction(ctx.message, '\N{OK HAND SIGN}')

    @commands.command(name='reload', pass_context=True)
    @checks.is_owner()
    async def _reload(self, ctx, *, module : str):
        """Reloads a module."""
        try:
            self.bot.unload_extension("cogs.%s" % module)
            self.bot.load_extension("cogs.%s" % module)
        except Exception as e:
            await self.bot.say('\N{PISTOL} \n {}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.add_reaction(ctx.message, '\N{OK HAND SIGN}')

    @commands.group(invoke_without_command=True)
    @checks.is_owner()
    async def echo(self, *, echo : str):
        """Echos whatever you say."""
        await self.bot.say(echo)

    @echo.command()
    @checks.is_owner()
    async def embed(self, *, echo : str):
        """Echos whatever you say as an embed."""
        message = discord.Embed(description=echo)
        await self.bot.say(embed=message)

def setup(bot):
    bot.add_cog(Admin(bot))
