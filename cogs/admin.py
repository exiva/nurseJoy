# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Admin(commands.Cog):
    """System commands"""

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        # clean up logic goes here
        pass

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

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
