# -*- coding: utf-8 -*-

import datetime
from discord.ext import tasks, commands
import discord


class Maintenance(commands.Cog):
    """
        Maintaince tasks run by Nurse Joy

        cleanTrades - Cleans trading post channels and deletes messages older
        than 7 days.
    """

    def __init__(self, bot):
        self.bot = bot
        self.cleantrades.start()

    def cog_unload(self):
        # clean up logic goes here
        pass

    async def cog_check(self, ctx):
        # checks that apply to every command in here
        return True

    async def bot_check(self, ctx):
        # checks that apply to every command to the bot
        return True

    async def bot_check_once(self, ctx):
        # check that apply to every command but is guaranteed to be called only once
        return True

    async def cog_command_error(self, ctx, error):
        # error handling to every command in here
        pass

    async def cog_before_invoke(self, ctx):
        # called before a command is called here
        pass

    async def cog_after_invoke(self, ctx):
        # called after a command is called here
        pass

    @tasks.loop(seconds=10)
    async def cleantrades(self):
        trades_channel = discord.utils.get(
            self.bot.get_all_channels(),
            guild__id=339074243838869504,
            name="trading-post",
        )

        await trades_channel.purge(
            before=datetime.datetime.utcnow() - timedelta(days=7),
            bulk=True,
            check=lambda m: not m.pinned,
        )

    @cleantrades.before_loop
    async def before_cleantrades(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Maintenance(bot))
