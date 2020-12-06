# -*- coding: utf-8 -*-

import aiohttp
import discord

from aiofile import AIOFile
from discord.ext import commands
from glob import glob
from os import path

class Deletelog(commands.Cog):
  """Log deleted messages and attachments."""
  
  def __init__(self, bot):
    self.logger = bot.logger
    self.logger.info(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.attachments:
      async with aiohttp.ClientSession() as session:
        for attachment in message.attachments:
          async with session.get(attachment.url) as resp:
            if resp.status != 200:
              return
            in_file, in_ext = path.splitext(attachment.filename)
            out_file = path.join('/tmp', f'{message.id}_{in_file}{in_ext}')
            async with AIOFile(out_file, 'wb') as fp:
              await fp.write(await resp.read())

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    ignoreUsers = [self.bot.user, self.bot.get_user(448855673623805966), self.bot.get_user(343128185744916520), self.bot.get_user(343127550752587788), self.bot.get_user(290601744042295296), self.bot.get_user(343122881024229377), self.bot.get_user(343127029857648640)]
    if not message.author in ignoreUsers:
      embed = discord.Embed(title='Message Deleted', color=discord.Colour.red())
      embed.add_field(name='Posted By', value=message.author)
      embed.add_field(name='User ID', value=message.author.id)
      embed.add_field(name='Deleted From', value=message.channel.name, inline=True)
      if message.content:
        embed.add_field(name='Message Content', value=message.content, inline=False)
      embed.set_thumbnail(url='https://i.imgur.com/bKeMCyG.png')
      delete_log = discord.utils.get(
        self.bot.get_all_channels(),
        guild__id=339074243838869504,
        name="delete-log",
      )
      files = glob(f"/tmp/{message.id}*")
      if files:
        attachments = []
        for file in files:
          embed.set_image(url=f"attachment://{path.basename(file)}")
          attachments.append(discord.File(file))
        await delete_log.send(embed=embed, files=attachments)
      else:
        await delete_log.send(embed=embed)


def setup(bot):
    bot.add_cog(Deletelog(bot))
