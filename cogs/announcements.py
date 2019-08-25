# -*- coding: utf-8 -*-

import asyncio
import discord
import urllib.request
from discord.ext import tasks, commands
from distutils.version import StrictVersion
from twitter import *

import aiohttp

class announcements(commands.Cog):
    """Announcements cog

       Posts Tweet announcements, and version forces

    """

    def __init__(self, bot):
        self.bot = bot
        self.t = Twitter(auth=OAuth(
                '***REMOVED***',
                '***REMOVED***',
                '***REMOVED***',
                '***REMOVED***'))
        self.twitters = [
            ['PokemonGoApp', False, None],
            ['chrales', True, None]
            ]
        self.currentVersion = "0.0.0"
        self.checkTweets.start()
        self.checkVersionForce.start()

    def cog_unload(self):
        print("Unloading announcements cog...")
        self.checkTweets.cancel()
        self.checkVersionForce.cancel()
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        self.ann_chan = discord.utils.get(
            self.bot.get_all_channels(),
            guild__id=339074243838869504,
            name="lab-1",
        )

    @tasks.loop(seconds=30)
    async def checkTweets(self):
        for user in self.twitters:
            tweets = self.t.statuses.user_timeline(screen_name=user[0])
            if not user[2]:
                user[2] = tweets[0]['id_str']
            elif user[2] != tweets[0]['id_str'] and (tweets[0]['in_reply_to_screen_name'] is None or tweets[0]['in_reply_to_screen_name'] == user[0]):
                msg = f"https://twitter.com/{user[0]}/status/{tweets[0]['id_str']}"
                if user[1]:  # Spoiler tweet
                    msg = f"|| {msg} ||"
                await self.ann_chan.send(msg)
            user[2] = tweets[0]['id_str']

    @tasks.loop(minutes=5)
    async def checkVersionForce(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pgorelease.nianticlabs.com/plfe/version") as resp:
                version = await resp.text('utf-8')
                version = version[2:]
                if self.currentVersion != "0.0.1" and StrictVersion(self.currentVersion) < StrictVersion(version):
                    await self.ann_chan.send(f"Pokemon Go update forced to version {version}. Check for updates in your App Store.")
                self.currentVersion = version

    # wait for bot to connect before starting tasks
    @checkTweets.before_loop
    async def before_checktweets(self):
        await self.bot.wait_until_ready()

    @checkVersionForce.before_loop
    async def before_checkVersionForce(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(announcements(bot))
