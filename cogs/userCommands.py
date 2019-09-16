# -*- coding: utf-8 -*-

import asyncio
from discord.ext import commands
import discord


class userCommands(commands.Cog):
  """
        Commands users can run
    """
  def __init__(self, bot):
    print(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot

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
    await asyncio.sleep(1 * 60)
    await ctx.message.delete()
    pass

  @commands.command()
  async def team(self, ctx, teamName: str):
    teams = ['instinct', 'mystic', 'valor']
    role = discord.utils.find(
        lambda m: teamName.lower() in m.name.lower(), ctx.message.guild.roles
    )
    roles = [r.name.lower() for r in ctx.message.author.roles]
    if teamName.lower() in teams:
      for u_role in roles:
        if u_role in teams:
          await ctx.send(
              content=
              f"Sorry {ctx.message.author.mention}, but you're already assigned to a team.",
              delete_after=1 * 60
          )
          return

      await ctx.message.author.add_roles(role)
      await ctx.send(
          content=
          f"{ctx.message.author.mention} I've set your team to {teamName.capitalize()}.",
          delete_after=1 * 60
      )
    else:
      await ctx.send(
          content=
          f"Sorry {ctx.message.author.mention}, `{teamName}` is not a valid team choice. Try again with `{ctx.prefix}{ctx.invoked_with} {', '.join(teams)}`",
          delete_after=1 * 60
      )


def setup(bot):
  bot.add_cog(userCommands(bot))
