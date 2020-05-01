# -*- coding: utf-8 -*-

import aiohttp
import discord
from discord.ext import tasks, commands
from distutils.version import StrictVersion
from peony import PeonyClient
from peony.exceptions import PeonyException
import math
import time
import datetime

class announcements(commands.Cog):
  """Announcements cog

       Posts Tweet announcements, and version forces

    """
  def __init__(self, bot):
    print(f"Loaded {self.__class__.__name__} cog")
    self.bot = bot
    self.tokens = bot.twitterTokens
    self.t = PeonyClient(
        consumer_key=self.tokens['consumer_key'],
        consumer_secret=self.tokens['consumer_secret'],
        access_token=self.tokens['access_token'],
        access_token_secret=self.tokens['access_secret'],
    )
    self.tweets = []
    self.twitters = [
        {'username': 'PokemonGoApp', 'spoiler': False, 'lastid': None},
        {'username': 'chrales', 'spoiler': True, 'lastid': None},
    ]
    self.currentVersion = "0.0.0"
    self.checkTweets.start()
    self.checkVersionForce.start()
    self.nestsRotated.start()

  def cog_unload(self):
    print("Unloading announcements cog...")
    self.checkTweets.cancel()
    self.checkVersionForce.cancel()
    self.nestsRotated.cancel()
    pass

  @commands.Cog.listener()
  async def on_ready(self):
    self.ann_chan = discord.utils.get(
        self.bot.get_all_channels(),
        guild__id=339074243838869504,
        name="announcements",
    )

  @tasks.loop(time=datetime.time(hour=23, minute=0))
  async def nestsRotated(self):
    if math.floor((time.time() - 1582693200) / 86400) % 14 == 0:
      await self.ann_chan.send("Nests have migrated! Report new sightings on <http://thesilphroad.com/atlas>")

  @tasks.loop(seconds=30)
  async def checkTweets(self):
    for user in self.twitters:
      try:
        tweets = await self.t.api.statuses.user_timeline.get(screen_name=user['username'], count=1)
        tweet = tweets[0]
        if not user['lastid']:
          tweets = await self.t.api.statuses.user_timeline.get(screen_name=user['username'], count=100)
          for tweet in tweets:
            self.tweets.append(tweet.id_str)
          user['lastid'] = tweet.id_str
        elif user['lastid'] != tweet.id_str and tweet.id_str not in self.tweets and tweet.in_reply_to_screen_name in (None, user['username']):
          msg = f"https://twitter.com/{user['username']}/status/{tweet.id_str}"
          if user['spoiler']:  # Spoiler tweet
            msg = f"|| {msg} ||"
          await self.ann_chan.send(msg)
        user['lastid'] = tweet.id_str
        self.tweets.append(tweet.id_str)
      except PeonyException:
        print("twitter exception")
      except Exception as e:
        print(f"Something else happened: {e}")

  @checkTweets.after_loop
  async def on_checkTweets_cancel(self):
    await self.t.close()

  @tasks.loop(minutes=5)
  async def checkVersionForce(self):
    async with aiohttp.ClientSession() as session:
      async with session.get("https://pgorelease.nianticlabs.com/plfe/version") as resp:
        version = await resp.text('utf-8')
        version = version[2:]
        if self.currentVersion != "0.0.0" and StrictVersion(self.currentVersion
                                                           ) < StrictVersion(version):
          await self.ann_chan.send(
              f"Pokemon Go update forced to version {version}. Check for updates in your App Store."
          )
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
