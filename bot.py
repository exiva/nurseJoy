#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import config

cogs = [
    'cogs.system',
    'cogs.announcements',
]

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', **kwargs)
        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(cog, exc))

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))
        await bot.change_presence(activity=discord.Game(name='at the Pokémon Center!'))


bot = Bot()
bot.run(config.token)
