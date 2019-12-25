# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import re

class Inviteclean(commands.Cog):
    """The description for Inviteclean goes here."""

    def __init__(self, bot):
        self.bot = bot

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

    @commands.Cog.listener()
    async def on_message(self, message):
        inviteurl = re.compile(r"(discord.gg|discordapp.com/invite|discord.me)(\S+)")
        allowedDiscords = [339074243838869504, 261360369681956864, 237964415822069760, 201304964495048704]
        for finding in inviteurl.finditer(message.content):
            invite = await self.bot.fetch_invite(finding.string, with_counts=False)
            if invite.guild.id not in allowedDiscords:
                await message.delete()

def setup(bot):
    bot.add_cog(Inviteclean(bot))
