# -*- coding: utf-8 -*-

from inspect import cleandoc
import typing
import pytz
from discord.ext import commands
from datetime import datetime
import discord


class Admin(commands.Cog):
    """System commands"""

    def __init__(self, bot):
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
        if module == 'admin':
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
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            if reason is None:
                await ctx.send(f"{ctx.author.mention}, you must specify a reason for the action.")
                return False

            await ctx.guild.kick(member, reason=reason)
            embed = discord.Embed(title="\U0001f97e User Kicked", color=int("ffff66", 16))
            embed.add_field(name='Member', value=f'{member.display_name}', inline=False)
            embed.add_field(name='Reason', value=f'{reason}', inline=False)
            embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=f"Kicked by {ctx.author.display_name} at {datetime.now().strftime('%d/%m/%y %I:%M:%S')}")
            await ctx.send(embed=embed)

            await member.send(cleandoc(f"""Hello,
                You were kicked from {ctx.message.guild} for **{reason}**. You are allowed to rejoin the server if you wish to. But you may be banned in the future.
                """))

        except Exception as e:
            print(e)

    @commands.command()
    async def ban(self, ctx, members: commands.Greedy[discord.Member],
                  days: typing.Optional[int] = 0, *, reason=None):
        try:
            if reason is None:
                await ctx.send(f"{ctx.author.mention}, you must specify a reason for the action.")
                return False

            for member in members:
                await ctx.guild.ban(discord.Object(id=member), reason=reason,
                                    delete_message_days=days)
                embed = discord.Embed(title="\u26d4 User Banned", color=int("ffff66", 16))
                embed.add_field(name='Member', value=f'{member.display_name}', inline=False)
                embed.add_field(name='Reason', value=f'{reason}', inline=False)
                if days > 0:
                    embed.add_field(name='Messages Removed', value=f'{days} days', inline=False)
                embed.set_footer(icon_url=ctx.author.avatar_url,
                                 text=f"Banned by {ctx.author.display_name} at {datetime.now().strftime('%d-%m-%y %I:%M:%S')}")
                await ctx.send(embed=embed)
                await member.send(cleandoc(f"""Hello,
                    You were banned from {ctx.message.guild} for **{reason}**.
                    """))
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Admin(bot))
