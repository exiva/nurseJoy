# -*- coding: utf-8 -*-

import asyncio
import discord
import urllib.request
from discord.ext import commands
from distutils.version import StrictVersion
from twitter import *


class annoncements(commands.Cog):
    """Announcements cog

       Posts Tweet announcements, and version forces

    """

    def __init__(self, bot):
        self.bot = bot
        self.t = Twitter(auth=OAuth(
                '630713-FUwZlUfwULM9OecKcCvFekk1t95YMk8KUC6Wl58IcAz',
                'zk8iIm8bft1OTm3C9TDjLnIwUP0TnPUk7uVNNppu43MLg',
                'O39ryCasRdZsyx2LYZIMq8Dnm',
                'MpiRNC0CaUGpZjwmFqdgrF6pFcvuVzDFQcey5h5Sm6kBvXIm51'))
        self.twitters = [
            ['PokemonGoApp', False, None],
            ['chrales', True, None]
            ]
        self.currentVersion = "0.0.0"

    def cog_unload(self):
        print("Unloading announcements module...")
        self.tweetTask.cancel()
        self.versionTask.cancel()

        pass

    @commands.Cog.listener()
    async def on_ready(self):
        self.announcements = self.bot.get_channel(345910796016156676)
        self.tweetTask = self.bot.loop.create_task(self.checkTweets())
        self.versionTask = self.bot.loop.create_task(self.checkVersionForce())

    async def checkTweets(self):
        try:
            while not self.bot.is_closed():
                for user in self.twitters:
                    tweets = self.t.statuses.user_timeline(screen_name="PokemonGoApp")
                    if not user[2]:
                        user[2] = tweets[0]['id_str']
                    elif user[2] != tweets[0]['id_str'] and tweets[0]['in_reply_to_screen_name'] is None:
                        msg = f"https://twitter.com/{user[0]}/status/{tweets[0]['id_str']}"
                        if user[1]:  # Spoiler tweet
                            msg = f"|| {msg} ||"
                        await self.announcements.send(msg)
                    user[2] = tweets[0]['id_str']
                await asyncio.sleep(30)
        except Exception as e:
            print(e)

    async def checkVersionForce(self):
        try:
            while not self.bot.is_closed():
                with urllib.request.urlopen('https://pgorelease.nianticlabs.com/plfe/version') as version:
                    version = version.read().decode('utf-8')[2:]
                    if self.currentVersion != "0.0.0" and StrictVersion(self.currentVersion) < StrictVersion(version):
                        await self.announcements.send(f"Pokemon Go update forced to version {version}. Check for updates in your App Store.")
                    self.currentVersion = version
                    await asyncio.sleep(300)
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(annoncements(bot))
