# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Newcog:
    """The description for Newcog goes here."""

    def __init__(self, bot):
        self.bot = bot

    def __unload(self):
        # clean up logic goes here
        pass

    async def __local_check(self, ctx):
        # checks that apply to every command in here
        return True

    async def __global_check(self, ctx):
        # checks that apply to every command to the bot
        return True

    async def __global_check_once(self, ctx):
        # check that apply to every command but is guaranteed to be called only once
        return True

    async def __error(self, ctx, error):
        # error handling to every command in here
        pass

    async def __before_invoke(self, ctx):
        # called before a command is called here
        pass

    async def __after_invoke(self, ctx):
        # called after a command is called here
        pass


def setup(bot):
    bot.add_cog(Newcog(bot))
