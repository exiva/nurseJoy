# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import re

class Inviteclean(commands.Cog):
    """The description for Inviteclean goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.inviteurl = re.compile(r"(?:https?://)?(?:www\.)?(?:discord(?:\.| |\[?\(?\"?'?dot'?\"?\)?\]?)?(?:gg|io|me|li)|discordapp\.com/invite)/+((?:(?!https?)[\w\d-])+)", flags=re.IGNORECASE)
        self.allowedDiscords = [339074243838869504, 261360369681956864, 237964415822069760, 201304964495048704]

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
        finding = re.findall(self.inviteurl, message.content)
        for find in finding:
            invite = await self.bot.fetch_invite(find, with_counts=False)
            if invite.guild.id not in self.allowedDiscords:
                await message.delete()

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.bot.get_channel(int(payload.data["channel_id"]))
        if 'content' in payload.data:
            finding = re.findall(self.inviteurl, payload.data['content'])
            for find in finding:
                invite = await self.bot.fetch_invite(find, with_counts=False)
                if invite.guild.id not in self.allowedDiscords:
                    message = await channel.fetch_message(payload.message_id)
                    await message.delete()


def setup(bot):
    bot.add_cog(Inviteclean(bot))
