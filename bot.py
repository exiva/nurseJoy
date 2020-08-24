#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import config

cogs = [
    'cogs.system',
    'cogs.announcements',
    'cogs.mod',
    'cogs.fuckinghemlock',
    'cogs.maintenance',
    'cogs.userCommands',
    'cogs.inviteclean',
]


class Bot(commands.Bot):
  def __init__(self, **kwargs):
    super().__init__(
      command_prefix=config.prefix,
      case_insensitive=True,
      activity=discord.Game(name="at the Pokémon Center"),
      **kwargs)

    self.twitterTokens = config.twitter_tokens

    for cog in cogs:
      try:
        self.load_extension(cog)
      except Exception as exc:
        print(
            'Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(
                cog, exc
            )
        )

  async def on_ready(self):
    print('Logged on as {0} (ID: {0.id})'.format(self.user))

  async def on_command_error(self, ctx, error):
    if isinstance(error, CommandNotFound):
      pass


bot = Bot()
bot.run(config.token)
