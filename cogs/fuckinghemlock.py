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
    self.bot = bot
    self.db_conn = self.bot.get_cog("hemlock_db")
    self.logger.info(f"Loaded {self.__class__.__name__} cog")

  
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

  @commands.command(hidden=True, aliases=["i","interested","interest","hmm","join","j","attend","omw","coming",
    "cominf","going","here","h","herr","arrive","arrived","present","check-in",
    "physically-here","physically-present","checkin","physicallyhere","physicallypresent",
    "please","p","please-invite","invite-pls","invitepls","invite-plz","inviteplz",
    "plz","pls","pleaseinvite","remote","r","home"])
  async def maybe(self, ctx):
    teams = set(['instinct', 'mystic', 'valor'])
    roles = set([r.name.lower() for r in ctx.message.author.roles])
    if not teams.intersection(roles):
      await ctx.send(f"{ctx.message.author.mention}, you don't have a team set. Please set your team by sending `!team instinct, mystic, or valor`.")
    
    if ctx.invoked_with in ["please","p","please-invite","invite-pls","invitepls","invite-plz","inviteplz","plz","pls","pleaseinvite","remote","r","home"]:
      rslt = await self.db_conn.execute_query(f"""SELECT `friend_code`, `in_game_name` FROM `User` WHERE `userSnowflake` = (%s)""", (ctx.message.author.id))
      self.logger.info(rslt)
      self.logger.info(bool(rslt[0][0]))
      if not rslt or (not rslt[0][0] or not rslt[0][1]):
        await ctx.send(f"{ctx.message.author.mention}, you don't have your friend code or in gane name setup in Hemlock, set them by sending `!ign your trainername` and `!fc your code` so others can invite you.")


  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.user_id in [448855958928752640, 448855673623805966]:
      return
    emojis = [687744604552167429, 687744744851243052, 687744766720344084, 742380909428342934, 704410930288787516]
    remote_emojis = [742380909428342934, 704410930288787516]
    channel = self.bot.get_guild(payload.guild_id).get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = message.guild.get_member(payload.user_id)
    if payload.emoji.id in emojis and payload.event_type == "REACTION_ADD":
      teams = set(['instinct', 'mystic', 'valor'])
      roles = set([r.name.lower() for r in user.roles])
      if not teams.intersection(roles):
        await channel.send(f"{user.mention}, you don't have a team set. Please set your team by sending `!team instinct, mystic, or valor`.")
    if payload.emoji.id in remote_emojis and payload.event_type == "REACTION_ADD":
      rslt = await self.db_conn.execute_query(f"""SELECT `friend_code`, `in_game_name` FROM `User` WHERE `userSnowflake` = (%s)""", (payload.user_id))
      if not rslt or (not rslt[0][0] or not rslt[0][1]):
        await channel.send(f"{user.mention}, you don't have your friend code or in gane name setup in Hemlock, set them by sending `!ign your trainername` and `!fc your code` so others can invite you.")

def setup(bot):
  bot.add_cog(fuckingHemlock(bot))
