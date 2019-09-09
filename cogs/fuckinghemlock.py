# -*- coding: utf-8 -*-

from discord.ext import commands
import asyncio
import discord


class fuckingHemlock(commands.Cog):
    """

        Run tasks to keep welcome channel at top. For some reason Hemlock
        moves the last used ongoing raids channel as default.

    """

    def __init__(self, bot):
        print(f"Loaded {self.__class__.__name__} cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        isRaidCat = discord.utils.find(lambda c: c.name.startswith("🖼"), channel.category.channels)
        if isRaidCat:
            welcomeChannel = discord.utils.get(
                self.bot.get_all_channels(),
                guild__id=339074243838869504,
                name="welcome",
            )
            await asyncio.sleep(1)
            await welcomeChannel.edit(position=0)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        isRaidCat = discord.utils.find(lambda c: c.name.startswith("🖼"), channel.category.channels)
        if isRaidCat:
            welcomeChannel = discord.utils.get(
                self.bot.get_all_channels(),
                guild__id=339074243838869504,
                name="welcome",
            )
            await asyncio.sleep(1)
            await welcomeChannel.edit(position=0)


def setup(bot):
    bot.add_cog(fuckingHemlock(bot))
