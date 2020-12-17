# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio
import asyncpg
from prettytable import PrettyTable
from prettytable import MARKDOWN
from datetime import datetime
import pytz
import sys

class Contest(commands.Cog):
  """The description for Contest goes here."""

  def __init__(self, bot):
    self.logger = bot.logger
    self.logger.info(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot
    self.db = bot.db

  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    try:
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
          poster = message.embeds[0].footer.icon_url.split("?uid=")[1]
          user = channel.guild.get_member(int(poster))
          if user.id == 222435142918995968:
            return
          async with self.db.acquire() as conn:
            qry = "INSERT INTO raids(uid, channelid) VALUES($1, $2)"
            await conn.execute(qry, user.id, channel.id)

            # get participation in contest
            usr_qry = "SELECT uid FROM holiday_contest WHERE uid = $1"
            rows = await conn.fetch(usr_qry, user.id)
            # not in db yet. add to db
            if not rows:
              qry = "INSERT INTO holiday_contest(uid) VALUES($1)"
              await conn.execute(qry, user.id)
            # award points
            point_qry = "UPDATE holiday_contest SET score = score + 2 where uid = $1"
            await conn.execute(point_qry, user.id)
          log = self.bot.get_channel(607287123409633283)
          await channel.send(f"{user.display_name}#{user.discriminator} earned 2 points for posting a raid")
          await log.send(f"{user.display_name}#{user.discriminator} earned 2 points for posting a raid")
    except Exception as e:
      self.logger.error(f"hoidaycontest: Listener Exception {e} Full stacktrace\n{sys.exc_info()}")
  
  @commands.command()
  async def leaderboard(self, ctx):
    try:
      async with self.db.acquire() as conn:
        qry = "SELECT uid,score FROM holiday_contest ORDER BY score DESC"
        rows = await conn.fetch(qry)
        output = "```md\n"
        x = PrettyTable()
        x.field_names = ["Rank.", "Points", "User"]

        for i, row in enumerate(rows):
          user = ctx.guild.get_member(int(row['uid']))
          # space = " "*8-(len(row['score']))-1
          # output += f"   {i+1}. | {space}{row['score']} | {user.display_name}#{user.discriminator}\n"
          x.add_row([i+1, row['score'], f"{user.display_name}#{user.discriminator}"])
        x.align['User'] = "l"
        x.align['Points'] = "r"
        x.align['Rank.'] = "l"
        x.set_style(MARKDOWN)
        output += f"{x}\n```"
        embed = discord.Embed(title='<:delibird:659477773655474206>:christmas_tree: Leaderboard | 2020 PGNC Holiday Contest :christmas_tree:<:delibird:659477773655474206>',
          color=discord.Colour.red(),
          description=output)
        end = datetime(2021, 1, 12)
        now = datetime.now()
        ends = end - now
        embed.add_field(name="Updated", value=f"{now.strftime('%d/%m/%Y %I:%M %p')}")

        embed.set_footer(text=f"Contest ends in {ends.days} days @ Midnight")
        await ctx.send(embed=embed)
    except Exception as e:
      self.logger.error(f"hoidaycontest: Listener Exception {e} Full stacktrace\n{sys.exc_info()}")


def setup(bot):
  bot.add_cog(Contest(bot))
