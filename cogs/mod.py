# -*- coding: utf-8 -*-

import pytz
from discord.ext import commands
from datetime import datetime
import discord
import re

class Mod(commands.Cog):
    """
        Moderator tools

    """

    def __init__(self, bot):
        print(f"Loaded {self.__class__.__name__} cog")
        self.bot = bot
        self.everyonetag = re.compile(r"@here|@everyone")

    def cog_unload(self):
        # clean up logic goes here
        pass

    async def cog_check(self, ctx):
        roles = [role.name for role in ctx.author.roles]
        if 'Admins' in roles or 'Mods' in roles:
            return True
        else:
            await ctx.send(f"access: PERMISSION DENIED....and...\n {ctx.author.mention} you didn't say the magic word!")

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
        if bool(self.everyonetag.match(message.content)) and not message.channel.permissions_for(message.author).mention_everyone:
            type = re.search(self.everyonetag, message.content)
            count = len(message.guild.members) if type.group(0) == '@everyone' else len(message.channel.members)
            await message.channel.send(f"I'm sorry, {message.author.mention} I can only heal 6 Pok\U000000e9mon at a time. {count} is too many.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="New Member", color=int("86eef0", 16))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Username', value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name='Nickname', value=member.display_name, inline=True)
        embed.add_field(name='Joined Discord', value=self.convert_time(member.created_at), inline=True)
        embed.add_field(name='Joined Server', value=self.convert_time(member.joined_at), inline=True)

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

        embed = discord.Embed(title=f"Member {'Left' if not banned else 'Banned'}", color=color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Username', value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name='Nickname', value=member.display_name, inline=True)
        embed.add_field(name='Joined Discord', value=self.convert_time(member.created_at), inline=True)
        embed.add_field(name='Joined Server', value=self.convert_time(member.joined_at), inline=True)
        if banned:
            auditLog = await member.guild.audit_logs(action=discord.AuditLogAction.ban, limit=1).flatten()
            embed.add_field(name='Banned By', value=auditLog[0].user)
        if banned.reason:
            embed.add_field(name='Ban Reason', value=banned.reason)

        member_log = discord.utils.get(
            self.bot.get_all_channels(),
            guild__id=339074243838869504,
            name="member-log",
        )
        await member_log.send(embed=embed)

    @commands.command(aliases=['uinfo'])
    async def userinfo(self, ctx, member: discord.Member):
        roles = [str(role) for role in member.roles[1:]]
        roles = ["None"] if len(roles) == 0 else reversed(roles)

        embed = discord.Embed(title="User Info", color=int("67C7E2", 16))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Username', value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name='Nickname', value=member.display_name, inline=True)
        embed.add_field(name='Joined Discord', value=self.convert_time(member.created_at), inline=True)
        embed.add_field(name='Joined Server', value=self.convert_time(member.joined_at), inline=True)
        embed.add_field(name="Roles", value=f"{', '.join(roles)}")
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f"Requested by {ctx.author.display_name} at {datetime.now().strftime('%m-%d-%y %I:%M:%S')}")
        await ctx.send(embed=embed)

    @userinfo.error
    async def uinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print(error)
            await ctx.send('I could not find that member.')

    @commands.command(aliases=['sinfo'])
    async def serverinfo(self, ctx):
        server = ctx.message.guild
        online = len([member for member in server.members if str(member.status) != "offline"])
        txtchannel_count = len([chn for chn in server.channels if type(chn) == discord.channel.TextChannel])
        voicechannel_count = len([chn for chn in server.channels if type(chn) == discord.channel.VoiceChannel])
        roles = reversed([str(role) for role in server.roles[1:]])
        emoji = [str(emoji) for emoji in server.emojis]

        embed = discord.Embed(title=f"{server} Server info", color=int("FF9933", 16))
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name='Server Region', value=server.region, inline=True)
        embed.add_field(name='Server Owner', value=server.owner, inline=True)

        embed.add_field(name='Server Created', value=self.convert_time(server.created_at), inline=True)

        embed.add_field(name='Total Users', value=len(server.members), inline=True)
        embed.add_field(name='Users Online', value=online, inline=True)

        embed.add_field(name='Roles', value=len(server.roles), inline=True)
        embed.add_field(name='Roles', value=', '.join(roles), inline=True)

        embed.add_field(name='Text Channels', value=txtchannel_count, inline=True)
        embed.add_field(name='Voice Channels', value=voicechannel_count, inline=True)

        embed.add_field(name='Emoticons', value=len(server.emojis))
        embed.add_field(name='Emoticons', value=', '.join(emoji), inline=True)

        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f"Requested by {ctx.author.display_name} at {datetime.now().strftime('%m-%d-%y %I:%M:%S')}")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Mod(bot))
