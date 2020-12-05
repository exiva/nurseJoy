# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import pytz
from discord.ext import commands
from datetime import datetime
from inspect import cleandoc
import discord
import re
import io


class Mod(commands.Cog):
  """
        Moderator tools

    """
  def __init__(self, bot):
    self.logger = bot.logger
    self.logger.info(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot
    self.everyonetag = re.compile(r"@here|@everyone", re.IGNORECASE)

  def cog_unload(self):
    # clean up logic goes here
    pass

  async def cog_check(self, ctx):
    roles = [role.name for role in ctx.author.roles]
    if 'Admins' in roles or 'Mods' in roles:
      return True
    # else:
    # await ctx.send(
    # f"access: PERMISSION DENIED....and...\n {ctx.author.mention} you didn't say the magic word!"
    # )

  async def cog_after_invoke(self, ctx):
    # called after a command is called here
    await ctx.message.delete()
    pass

  def convert_time(self, t):
    timezone = pytz.timezone('America/New_York')
    t = pytz.timezone("UTC").localize(t).astimezone(timezone)
    return t.__format__('%m/%d/%Y %I:%M %p')

  @commands.Cog.listener()
  async def on_message(self, message):
    if bool(re.search(self.everyonetag, message.content)
           ) and not message.channel.permissions_for(message.author).mention_everyone:
      type = re.search(self.everyonetag, message.content)
      count = len(message.guild.members
                 ) if type.group(0) == '@everyone' else len(message.channel.members)
      await message.channel.send(
          f"I'm sorry, {message.author.mention} I can only heal 6 Pok\U000000e9mon at a time. {count} is too many."
      )

  @commands.Cog.listener()
  async def on_member_join(self, member):
    embed = discord.Embed(title="New Member", color=int("86eef0", 16))
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(
        name='Username', value=f"{member.name}#{member.discriminator}", inline=True
    )
    embed.add_field(name='Nickname', value=member.display_name, inline=True)
    embed.add_field(
        name='Joined Discord', value=self.convert_time(member.created_at), inline=True
    )
    embed.add_field(
        name='Joined Server', value=self.convert_time(member.joined_at), inline=True
    )

    member_log = discord.utils.get(
        self.bot.get_all_channels(),
        guild__id=339074243838869504,
        name="member-log",
    )
    await member_log.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    banList = await member.guild.bans()
    banned = discord.utils.find(lambda u: u.user.id == member.id, banList)
    color = discord.Colour.dark_magenta() if banned else discord.Colour.magenta()

    embed = discord.Embed(
        title=f"Member {'Left' if not banned else 'Banned'}", color=color
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(
        name='Username', value=f"{member.name}#{member.discriminator}", inline=True
    )
    embed.add_field(name='Nickname', value=member.display_name, inline=True)
    embed.add_field(
        name='Joined Discord', value=self.convert_time(member.created_at), inline=True
    )
    embed.add_field(
        name='Joined Server', value=self.convert_time(member.joined_at), inline=True
    )
    if banned:
      auditLog = await member.guild.audit_logs(
          action=discord.AuditLogAction.ban, limit=1
      ).flatten()
      embed.add_field(name='Banned By', value=auditLog[0].user)
      if banned.reason:
        embed.add_field(name='Ban Reason', value=banned.reason)

    member_log = discord.utils.get(
        self.bot.get_all_channels(),
        guild__id=339074243838869504,
        name="member-log",
    )
    await member_log.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_update(self, before, after):
    if before.nick == after.nick:
      return
    embed = discord.Embed(title="Member Changed Nickname", color=int("86eef0", 16))
    embed.set_thumbnail(url=before.avatar_url)
    embed.add_field(
        name='Username', value=f"{before.name}#{before.discriminator}", inline=True
    )
    embed.add_field(name='Nickname Change', value=f"`{before.nick}` to `{after.nick}`")
    member_log = discord.utils.get(
      self.bot.get_all_channels(),
      guild__id=339074243838869504,
      name="member-log",
    )
    await member_log.send(embed=embed)

  @commands.Cog.listener()
  async def on_user_update(self, before, after):
    member_log = discord.utils.get(
      self.bot.get_all_channels(),
      guild__id=339074243838869504,
      name="member-log",
    )

    if before.name != after.name:
      embed = discord.Embed(title="Member Changed Username", color=int("86eef0", 16))
      embed.set_thumbnail(url=before.avatar_url)
      embed.add_field(
        name='Username', value=f"{before.name}#{before.discriminator}", inline=True
        )
      embed.add_field(name='Username Change', value=f"`{before.name}` to `{after.name}`")
      await member_log.send(embed=embed)

    if before.avatar != after.avatar:
      embed = discord.Embed(title="Member Changed Avatar", color=int("86eef0", 16))
      embed.set_thumbnail(url=before.avatar_url)
      embed.add_field(
        name='Username', value=f"{after.name}#{after.discriminator}", inline=True
        )
      embed.set_image(url=after.avatar_url)
      await member_log.send(embed=embed)

  @commands.command(aliases=['uinfo'])
  async def userinfo(self, ctx, member: discord.Member):
    roles = [str(role) for role in member.roles[1:]]
    roles = ["None"] if len(roles) == 0 else reversed(roles)

    embed = discord.Embed(title="User Info", color=int("67C7E2", 16))
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(
        name='Username', value=f"{member.name}#{member.discriminator}", inline=True
    )
    embed.add_field(name='Nickname', value=member.display_name, inline=True)
    embed.add_field(
        name='Joined Discord', value=self.convert_time(member.created_at), inline=True
    )
    embed.add_field(
        name='Joined Server', value=self.convert_time(member.joined_at), inline=True
    )
    embed.add_field(name="Roles", value=f"{', '.join(roles)}")
    embed.set_footer(
        icon_url=ctx.author.avatar_url,
        text=
        f"Requested by {ctx.author.display_name} at {datetime.now().strftime('%m-%d-%y %I:%M:%S')}"
    )
    await ctx.send(embed=embed)

  @userinfo.error
  async def uinfo_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send('I could not find that member.')

  @commands.command(aliases=['sinfo'])
  async def serverinfo(self, ctx):
    server = ctx.message.guild
    online = len(
        [member for member in server.members if str(member.status) != "offline"]
    )
    txtchannel_count = len(
        [chn for chn in server.channels if type(chn) == discord.channel.TextChannel]
    )
    voicechannel_count = len(
        [chn for chn in server.channels if type(chn) == discord.channel.VoiceChannel]
    )
    roles = reversed([str(role) for role in server.roles[1:]])
    emoji = [str(emoji) for emoji in server.emojis]

    embed = discord.Embed(title=f"{server} Server info", color=int("FF9933", 16))
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name='Server Region', value=server.region, inline=True)
    embed.add_field(name='Server Owner', value=server.owner, inline=True)

    embed.add_field(
        name='Server Created', value=self.convert_time(server.created_at), inline=True
    )

    embed.add_field(name='Server Features', value=', '.join(server.features).lower(), inline=True)
  
    embed.add_field(name='Server Boosts', value=server.premium_subscription_count)
    embed.add_field(name='Server Boost Level', value=server.premium_tier)

    embed.add_field(name='Total Users', value=len(server.members), inline=True)
    embed.add_field(name='Users Online', value=online, inline=True)

    embed.add_field(name='Total Roles', value=len(server.roles), inline=True)
    embed.add_field(name='Roles', value=', '.join(roles), inline=True)

    embed.add_field(name='Text Channels', value=txtchannel_count, inline=True)
    embed.add_field(name='Voice Channels', value=voicechannel_count, inline=True)

    embed.add_field(name='Total Categories', value=len(server.categories))
    
    embed.add_field(name='Total Emoticons', value=f"{len(server.emojis)}/{server.emoji_limit}")

    for i in range(0, len(emoji), 10):
      embed.add_field(name=f'Emoticons', value=' '.join(emoji[i:i+10]), inline=True)

    embed.set_footer(
        icon_url=ctx.author.avatar_url,
        text=
        f"Requested by {ctx.author.display_name} at {datetime.now().strftime('%m-%d-%y %I:%M:%S')}"
    )

    await ctx.send(embed=embed)

  @commands.command()
  async def say(self, ctx, channel: commands.Greedy[discord.TextChannel], *, message: str):
    for c in channel:
      if ctx.message.attachments:
        files = []
        async with aiohttp.ClientSession() as session:
          for attachment in ctx.message.attachments:
            async with session.get(attachment.proxy_url) as resp:
              if resp.status != 200:
                return self.logger.warn("Couldn't download image.")
              img = io.BytesIO(await resp.read())
              filename = attachment.filename
              files.append(discord.File(img, filename))
        msg = await c.send(content=message, files=files)
      else:
        msg = await c.send(content=message)
      
      if c.is_news():
        await msg.publish()

  @commands.command()
  async def kick(self, ctx, member: discord.Member, *, reason=None):
    try:
      if reason is None:
        await ctx.send(
            f"{ctx.author.mention}, you must specify a reason for the action."
        )
        return False

      try:
        await member.send(
          cleandoc(
              f"""Hello,
                You were kicked from {ctx.message.guild} for **{reason}**. 
                
                You are allowed to rejoin the server if you wish to, but you may be banned in the future.
                """
          )
        )
      except discord.Forbidden:
        self.logger.info(f"Cannot message {member}")

      await ctx.guild.kick(member, reason=reason)
      embed = discord.Embed(title="\U0001f97e User Kicked", color=int("ffff00", 16))
      embed.add_field(name='Member', value=f'{member.display_name}', inline=False)
      embed.add_field(name='Reason', value=f'{reason}', inline=False)
      embed.set_footer(
          icon_url=ctx.author.avatar_url,
          text=
          f"Kicked by {ctx.author.display_name} at {datetime.now().strftime('%d/%m/%y %I:%M:%S')}"
      )
      await ctx.send(embed=embed)

      await member.send(
          cleandoc(
              f"""Hello,
                You were kicked from {ctx.message.guild} for **{reason}**. You are allowed to rejoin the server if you wish to. But you may be banned in the future.
                """
          )
      )

    except Exception as e:
      self.logger.error(e)

  @commands.command()
  async def ban(self, ctx, member: discord.Member, days: int = 0, *, reason=None):
    try:
      if reason is None:
        await ctx.send(
            f"{ctx.author.mention}, you must specify a reason for the ban."
        )
        return False

      try:
        await member.send(f"You were banned from {ctx.message.guild} for **{reason}**.")
      except discord.Forbidden:
        self.logger.info(f"Cannot message {member}")
      
      await ctx.guild.ban(user=member, reason=reason, delete_message_days=days)
      embed = discord.Embed(title="\U0001f97e User Banned", color=int("ff0000", 16))
      embed.add_field(name='Member', value=f'{member.display_name}', inline=False)
      embed.add_field(name='Reason', value=f'{reason}', inline=False)
      embed.set_footer(
          icon_url=ctx.author.avatar_url,
          text=
          f"Kicked by {ctx.author.display_name} at {datetime.now().strftime('%d/%m/%y %I:%M:%S')}"
      )
      await ctx.send(embed=embed)


    except Exception as e:
      self.logger.error(e)

  @commands.command()
  async def mute(self, ctx, member: discord.Member, time: int = 10, *, reason=None):
    log_chn = discord.utils.get(
        self.bot.get_all_channels(),
        guild__id=339074243838869504,
        name="member-log",
      )

    embed = discord.Embed(title='Member Muted', color=discord.Colour.red())
    embed.add_field(name='Muted Member', value=f"{member.name}#{member.discriminator}")
    embed.add_field(name='Muted By', value=ctx.message.author)
    embed.add_field(name='Length', value=time)
    embed.add_field(name='Reason', value=f"{reason if reason else 'None Provided'}")

    for c in ctx.guild.channels:
      await c.set_permissions(member,
            send_messages=False,
            add_reactions=False
            )
    
    await log_chn.send(embed=embed)
    await ctx.send(f"{member.mention} you have been muted for {time} minutes.")

    await asyncio.sleep(time * 60)
    for c in ctx.guild.channels:
      await c.set_permissions(member, overwrite=None)


def setup(bot):
  bot.add_cog(Mod(bot))
