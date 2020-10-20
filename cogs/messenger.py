# -*- coding: utf-8 -*-


from discord.ext import commands
import asyncio
import logging
import discord


class messenger(commands.Cog):

  def __init__(self, bot):
    self.logger = bot.logger
    self.logger.info(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot

  async def cog_check(self, ctx):
    return await self.bot.is_owner(ctx.author)

  @commands.Cog.listener()
  async def on_message(self, message):
    msg_chan = discord.utils.get(
        self.bot.get_all_channels(),
        guild__id=339074243838869504,
        name="joy-messages",
    )
    if message.guild is None and message.author != self.bot.user:
      embed = discord.Embed(title="New Message", color=int("ff00ff", 16))
      embed.set_thumbnail(url=message.author.avatar_url)
      embed.add_field(name="From", value=f"{message.author}")
      embed.add_field(name="Message", value=f"{message.content}")
      embed.set_footer(text=f"To reply use !reply {message.author.name}#{message.author.discriminator} message")
      await msg_chan.send(embed=embed)
      await message.author.trigger_typing()
      await asyncio.sleep(4)
      await message.author.send("Thanks for your message. You'll get a reply soon.")

  @commands.command()
  async def reply(self, ctx, member: discord.Member, *, message: str):
    await member.trigger_typing()
    await asyncio.sleep(5)
    await member.send(f"{ctx.message.author.display_name}: {message}")


def setup(bot):
  bot.add_cog(messenger(bot))
