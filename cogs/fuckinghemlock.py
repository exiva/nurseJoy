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
    self.logger = bot.logger
    self.logger.info(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot
    self.raidcommands = ["i","interested","interest","hmm","join","j","attend","omw","coming",
    "cominf","going","here","h","herr","arrive","arrived","present","check-in",
    "physically-here","physically-present","checkin","physicallyhere","physicallypresent",
    "please","p","please-invite","invite-pls","invitepls","invite-plz","inviteplz",
    "plz","pls","pleaseinvite","invitepls","inviteplz","remote","r","home"]
  
  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    isRaidCat = discord.utils.find(
        lambda c: c.name.startswith("\U0001f5bc"), channel.category.channels
    )
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
    isRaidCat = discord.utils.find(
        lambda c: c.name.startswith("\U0001f5bc"), channel.category.channels
    )
    if isRaidCat:
      welcomeChannel = discord.utils.get(
          self.bot.get_all_channels(),
          guild__id=339074243838869504,
          name="welcome",
      )
      await asyncio.sleep(1)
      await welcomeChannel.edit(position=0)

  @commands.command(hidden=True, aliases=self.raidcommands)
  async def maybe(self, ctx):
    teams = set(['instinct', 'mystic', 'valor'])
    roles = set([r.name.lower() for r in ctx.message.author.roles])
    if not teams.intersection(roles):
      await ctx.send(f"{ctx.message.author.mention}, you don't have a team set. Please set your team by sending `!team instinct, mystic, or valor`.")


def setup(bot):
  bot.add_cog(fuckingHemlock(bot))
