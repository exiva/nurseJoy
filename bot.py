#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import config
import logging
import asyncpg

cogs = [
    'cogs.system',
    'cogs.hemlockdb',
    'cogs.announcements',
    'cogs.mod',
    'cogs.fuckinghemlock',
    'cogs.maintenance',
    'cogs.userCommands',
    'cogs.inviteclean',
    'cogs.deletelog',
    'cogs.messenger',
    'cogs.pganfeed',
    'cogs.holidaycontest',
]

async def init():
  db = await asyncpg.create_pool(**config.creds)

  try:
    bot = Bot(db=db)
    await bot.start(config.token)
  except KeyboardInterrupt:
    await bot.logout()


class Bot(commands.Bot):
  def __init__(self, **kwargs):
    super().__init__(
      command_prefix=config.prefix,
      case_insensitive=True,
      activity=discord.Game(name="at the Pokémon Center"),
      intents=discord.Intents.all(),
      **kwargs)
    self.db = kwargs.pop("db")

    self.logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    self.disc_logger = logging.getLogger('discord')
    self.disc_logger.setLevel(logging.ERROR)
    self.peony_logger = logging.getLogger('peony')
    self.peony_logger.setLevel(logging.ERROR)
    
    self.config = config
    self.twitterTokens = config.twitter_tokens

    for cog in cogs:
      try:
        self.load_extension(cog)
      except Exception as exc:
        self.logger.error(f"Cog {cog} due to {exc.__class__.__name__}: {exc}")

  async def on_ready(self):
    self.logger.info(f"Logged on as {self.user} (ID: {self.user.id})")
    self.logger.info(f"Using discord.py {discord.__version__}")

  async def on_command_error(self, ctx, error):
    if isinstance(error, CommandNotFound):
      pass


loop = asyncio.get_event_loop()
loop.run_until_complete(init())