# -*- coding: utf-8 -*-

from discord.ext import commands
import asyncio
import discord
import asyncpg
import sys

class fuckingHemlock(commands.Cog):
  """

        Run tasks to keep welcome channel at top. For some reason Hemlock
        moves the last used ongoing raids channel as default.

    """
  def __init__(self, bot):
    self.logger = bot.logger
    self.bot = bot
    self.db_conn = self.bot.get_cog("hemlock_db")
    self.db = bot.db
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
    try:
      async with self.db.acquire() as conn:
        #### Holiday Contest
        qry = "SELECT attendees FROM raids WHERE channelid = $1"
        rows = await conn.fetch(qry, ctx.channel.id)
        if ctx.author.id not in rows[0]['attendees']:
          update_query = "UPDATE raids SET attendees = array_append(attendees, $1) WHERE channelid = $2"
          await conn.execute(update_query, ctx.author.id, ctx.channel.id)
          if ctx.author.id == 222435142918995968:
            return
          # get participation in contest
          usr_qry = "SELECT uid FROM holiday_contest WHERE uid = $1"
          rows = await conn.fetch(usr_qry, ctx.author.id)
          # not in db yet. add to db
          if not rows:
            qry = "INSERT INTO holiday_contest(uid) VALUES($1)"
            await conn.execute(qry, ctx.author.id)
          # award points
          point_qry = "UPDATE holiday_contest SET score = score + 1 where uid = $1"
          await conn.execute(point_qry, ctx.author.id)
          log = self.bot.get_channel(607287123409633283)
          await ctx.send(f"{ctx.author.display_name}#{ctx.author.discriminator} earned 1 points for joining a raid")
          await log.send(f"{ctx.author.display_name}#{ctx.author.discriminator} earned 1 points for joining a raid")
    except Exception as e:
      self.logger.error(f"fuckinghemlock: Command Exception {e} Full stacktrace\n{sys.exc_info()}")

    teams = set(['instinct', 'mystic', 'valor'])
    roles = set([r.name.lower() for r in ctx.message.author.roles])
    if not teams.intersection(roles):
      await ctx.send(f"{ctx.message.author.mention}, you don't have a team set. Please set your team by sending `!team instinct, mystic, or valor`.")
    
    if ctx.invoked_with in ["please","p","please-invite","invite-pls","invitepls","invite-plz","inviteplz","plz","pls","pleaseinvite","remote","r","home"]:

      rslt = await self.db_conn.execute_query(f"""SELECT `friend_code`, `in_game_name` FROM `User` WHERE `userSnowflake` = (%s)""", (ctx.message.author.id))
      if not rslt or (not rslt[0][0] or not rslt[0][1]):
        await ctx.send(f"{ctx.message.author.mention}, you don't have your friend code or in game name setup in Hemlock, set them by sending `!ign your trainername` and `!fc your code` so others can invite you.")


  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.user_id in [448855958928752640, 448855673623805966, 222435142918995968]:
      return
    emojis = [687744604552167429, 687744744851243052, 687744766720344084, 742380909428342934, 704410930288787516]
    remote_emojis = [742380909428342934, 704410930288787516]
    channel = self.bot.get_guild(payload.guild_id).get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = message.guild.get_member(payload.user_id)
    if payload.emoji.id in emojis and payload.event_type == "REACTION_ADD":
      try:
        async with self.db.acquire() as conn:
          #### Holiday Contest
          qry = "SELECT attendees FROM raids WHERE channelid = $1"
          rows = await conn.fetch(qry, payload.channel_id)
          if user.id not in rows[0]['attendees']:
            update_query = "UPDATE raids SET attendees = array_append(attendees, $1) WHERE channelid = $2"
            await conn.execute(update_query, user.id, payload.channel_id)
            # get participation in contest
            if user.id == 222435142918995968:
              return
            usr_qry = "SELECT uid FROM holiday_contest WHERE uid = $1"
            rows = await conn.fetch(usr_qry, user.id)
            # not in db yet. add to db
            if not rows:
              qry = "INSERT INTO holiday_contest(uid) VALUES($1)"
              await conn.execute(qry, user.id)
            # award points
            point_qry = "UPDATE holiday_contest SET score = score + 1 where uid = $1"
            await conn.execute(point_qry, user.id)
            log = self.bot.get_channel(607287123409633283)
            await channel.send(f"{user.display_name}#{user.discriminator} earned 1 points for joining a raid")
            await log.send(f"{user.display_name}#{user.discriminator} earned 1 points for joining a raid")
      except Exception as e:
        self.logger.error(f"fuckinghemlock: Reaction Exception {e} Full stacktrace\n{sys.exc_info()}")

      teams = set(['instinct', 'mystic', 'valor'])
      roles = set([r.name.lower() for r in user.roles])
      if not teams.intersection(roles):
        await channel.send(f"{user.mention}, you don't have a team set. Please set your team by sending `!team instinct, mystic, or valor`.")
    if payload.emoji.id in remote_emojis and payload.event_type == "REACTION_ADD":
      rslt = await self.db_conn.execute_query(f"""SELECT `friend_code`, `in_game_name` FROM `User` WHERE `userSnowflake` = (%s)""", (payload.user_id))
      if not rslt or (not rslt[0][0] or not rslt[0][1]):
        await channel.send(f"{user.mention}, you don't have your friend code or in game name setup in Hemlock, set them by sending `!ign your trainername` and `!fc your code` so others can invite you.")

def setup(bot):
  bot.add_cog(fuckingHemlock(bot))
