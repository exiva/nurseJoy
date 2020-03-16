# -*- coding: utf-8 -*-

import asyncio
import datetime
from datetime import timedelta
from discord.ext import tasks, commands
import discord
import json
import io
import urllib
import aiohttp
import polyline


class Maintenance(commands.Cog):
  """
        Maintaince tasks run by Nurse Joy

        cleanTrades - Cleans trading post channels and deletes messages older
        than 7 days.

        clearRaidBoards - Cleans raid board channels at midnight.
    """
  def __init__(self, bot):
    print(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot
    self.cleantrades.start()
    self.bottomPinned.start()
    self.clearRaidBoards.start()

  def cog_unload(self):
    self.cleantrades.cancel()()
    self.bottomPinned.cancel()
    self.clearRaidBoards.cancel()
    # clean up logic goes here
    pass

  async def cog_check(self, ctx):
    roles = [role.name for role in ctx.author.roles]
    if 'Admins' in roles:
      return True
    # else:
      # await ctx.send(
          # f"access: PERMISSION DENIED....and...\n {ctx.author.mention} you didn't say the magic word!"
      # )

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

  @tasks.loop(seconds=10)
  async def bottomPinned(self):
    raidBoards = filter(
        lambda ch: ch.name.startswith("\U0001f5bc"), self.bot.get_all_channels()
    )

    def deleteCheck(m):
      if m.author == self.bot.user and not m.pinned:
        return True

    for raidBoard in raidBoards:
      messages = await raidBoard.history(limit=1).flatten()
      for m in messages:
        if m.author != self.bot.user:
          chatChannel = discord.utils.find(
              lambda c: c.name.endswith("-chat"), raidBoard.category.channels
          )
          await raidBoard.purge(limit=100, check=deleteCheck)
          await raidBoard.send(
              f"Please **only** use this channel for posting in-game screenshots of gyms with raid eggs/bosses or commands for raids, and keep chat in the appropriate raid channel or <#{chatChannel.id}>.\n\nMap screenshots do not work with the Raid bot. To start a raid manually type `!raid Tier Number or Boss Gym Name`"
          )

  @tasks.loop(time=datetime.time(hour=4, minute=0))
  async def clearRaidBoards(self):
    print("Clearing raid boards")
    raidBoards = filter(
        lambda ch: ch.name.startswith("\U0001f5bc"), self.bot.get_all_channels()
    )

    def deleteCheck(m):
      if (m.author.display_name == "Professor Hemlock" and
          m.embeds) and (m.embeds[0].author):
        return not m.embeds[0].author.name.startswith("EX ")
      elif m.author == self.bot.user:
        return False
      else:
        return True

    for raidBoard in raidBoards:
      await raidBoard.purge(limit=100, check=deleteCheck)

  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    isRaidCat = discord.utils.find(
        lambda c: c.name.startswith("\U0001f5bc"), channel.category.channels
    )

    def isHemlock(msg):
      if msg.channel == channel and msg.author.display_name == "Professor Hemlock" and msg.embeds:
        return msg

    if isRaidCat:
      try:
        message = await self.bot.wait_for('message', check=isHemlock)
      except asyncio.TimeoutError:
        pass
      else:
        await channel.send(
            "**Note**: This channel will self destruct after the raid has completed. Only use this channel for raid coordination."
        )
        if message.embeds[0].title is not discord.Embed.Empty:
          await channel.send(
              f"To get automatically alerted of raids at {message.embeds[0].title} in the future, send `!notify gym {message.embeds[0].title}` in <#{isRaidCat.id}>"
          )
        await channel.send("__**COVID-19 Warning**__\nDuring the COVID-19 pandemic, please keep raid groups as small as possible. Practice social distancing staying 4 to 6 feet apart from each other if you cannot stay in vehicles during raids. Make use of the voice chat channels to keep distance from others. If you have any symptoms, stay home, Pokémon isn't worth spreading the virus.\n\nUpdates on the New York state of health can be found here https://www.health.ny.gov/diseases/communicable/coronavirus/")
  
  @commands.command()
  async def initchannels(self, ctx):
    raidBoards = filter(
        lambda ch: ch.name.startswith("\U0001f5bc"), self.bot.get_all_channels()
    )
    try:
      for raidBoard in raidBoards:
        await raidBoard.purge(bulk=True)
        with open(f'channels/{raidBoard.id}.json', 'r') as channel:
          channelconfig = json.load(channel)
          poly = urllib.parse.quote((polyline.encode(channelconfig['bounds'])))
          url = "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/path-3+{}-0.5+{}-0.3({})/auto/500x300@2x?access_token=pk.eyJ1IjoiZGl2aW5hdHVtIiwiYSI6ImNrMDkzNWZjdjA0bHgzZG1xN283azV2bTcifQ._RTYtDdjm0pIXINNbQBsHQ".format(
              channelconfig['color'], channelconfig['color'], poly
          )
          async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
              if resp.status != 200:
                return print("Couldn't download image.")
              img = io.BytesIO(await resp.read())

              embed = discord.Embed(
                  title=f"This raid board covers the following regions",
                  description=channelconfig['regions'],
                  color=int(channelconfig['color'], 16)
              )
              embed.set_image(url="attachment://map.png")
              sendembed = await raidBoard.send(
                  file=discord.File(img, 'map.png'), embed=embed
              )

              await sendembed.pin()
    except Exception as e:
      print(f"{e.__class__.__name__} {e}")


def setup(bot):
  bot.add_cog(Maintenance(bot))
