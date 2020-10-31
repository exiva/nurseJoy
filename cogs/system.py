# -*- coding: utf-8 -*-

import asyncio
import typing
import pytz
from discord.ext import commands
from datetime import datetime
import discord
import subprocess


class System(commands.Cog):
  """
    System commands

    """
  def __init__(self, bot):
    self.logger = bot.logger
    self.logger.info(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot

  def cog_unload(self):
    # clean up logic goes here
    pass

  async def cog_check(self, ctx):
    return await self.bot.is_owner(ctx.author)

  def convert_time(self, t):
    timezone = pytz.timezone('America/New_York')
    t = pytz.timezone("UTC").localize(t).astimezone(timezone)
    return t.__format__('%m/%d/%Y %I:%M %p')

  @commands.command()
  async def load(self, ctx, *, module):
    try:
      self.bot.load_extension(f"cogs.{module}")
    except Exception as e:
      await ctx.send(e)

  @commands.command()
  async def unload(self, ctx, *, module):
    if module == str(self.__cog_name__).lower():
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

  @commands.command()
  async def reloadall(self, ctx):
    cogs = [cog.__module__.split('.')[1] for cog in self.bot.cogs.values()]
    for cog in cogs:
      try:
        self.bot.unload_extension(f"cogs.{cog}")
        self.bot.load_extension(f"cogs.{cog}")
      except Exception as e:
        await ctx.send(f"Error loading {cog}: {e}")
    await ctx.send()

  @commands.command()
  async def update(self, ctx):
    result = subprocess.check_output(['git', 'pull'])
    await ctx.send(result.decode('utf-8'))

  @commands.command()
  async def clear(self, ctx):
    msg = await ctx.send(f"Would you really like to clear **all** messages?")
    await msg.add_reaction('\U0001F44D')
    await msg.add_reaction('\U0001F44E')

    def check(reaction, user):
      return user == ctx.message.author and str(reaction.emoji) == '\U0001F44D'

    try:
      reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=5.0)
    except asyncio.TimeoutError:
      await msg.delete()
      return
    else:
      await ctx.channel.purge(bulk=True, limit=9000)

  @commands.command()
  async def sclear(self, ctx):
    msg = await ctx.send(
        f"Would you really like to clear everything but pinned messages?"
    )
    await msg.add_reaction('\U0001F44D')
    await msg.add_reaction('\U0001F44E')

    def check(reaction, user):
      return user == ctx.message.author and str(reaction.emoji) == '\U0001F44D'

    def deleteCheck(message):
      return not message.pinned

    try:
      reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=5.0)
    except asyncio.TimeoutError:
      await msg.delete()
      return
    else:
      await ctx.channel.purge(bulk=True, limit=9000, check=deleteCheck)

def setup(bot):
  bot.add_cog(System(bot))
