# -*- coding: utf-8 -*-

from discord.ext import tasks, commands
import discord

class Pganfeed(commands.Cog):
  """The description for Dev goes here."""
  def __init__(self, bot):
    self.logger = bot.logger
    self.bot = bot
    self.bottomPin.start()

  def cog_unload(self):
    # clean up logic goes here
    pass

  async def cog_check(self, ctx):
    # checks that apply to every command in here
    return True

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

  @tasks.loop(seconds=5)
  async def bottomPin(self):
    try:
      trades_channel = discord.utils.get(
          self.bot.get_all_channels(),
          guild__id=339074243838869504,
          name="90-98-ivs",
      )
      def deleteCheck(m):
        if m.author == self.bot.user and not m.pinned:
          return True

      messages = await trades_channel.history(limit=11).flatten()
      await trades_channel.purge(limit=100, before=messages[-1])
      if messages[0].author != self.bot.user:
        await trades_channel.purge(limit=100, check=deleteCheck)
        await trades_channel.send("This is a _preview_ feed of the last 10 90-98% IV alerts from PoGo Alerts Network for Nassau County. To get a full access to a personal tailored feed, subscribe to the premium tier plan at <https://www.pogoalerts.net/pricing>")
    except Exception as e:
      pass


def setup(bot):
  bot.add_cog(Pganfeed(bot))
