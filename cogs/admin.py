# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Admin:
    """System commands"""

    def __init__(self, bot):
        self.bot = bot

    def __unload(self):
        # clean up logic goes here
        pass

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    async def __error(self, ctx, error):
        # error handling to every command in here
        pass

    async def __before_invoke(self, ctx):
        # called before a command is called here
        pass

    async def __after_invoke(self, ctx):
        # called after a command is called here
        pass

    @commands.command()
    async def load(self, ctx, *, module):
        try:
            self.bot.load_extension(f"cogs.{module}")
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def unload(self, ctx, *, module):
        if module == 'admin':
            await ctx.send("Can't unload system module.")
            return True
        try:
            self.bot.unload_extension(f"cogs.{module}")
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def reload(self, ctx, *, module):
        try:
            self.bot.unload_extension(f"cogs.{module}")
            self.bot.load_extension(f"cogs.{module}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down.")
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Admin(bot))
