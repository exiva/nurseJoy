# -*- coding: utf-8 -*-
import asyncio
from discord.ext import commands
import discord
import aiomysql
import logging

class hemlock_db(commands.Cog):
    """Class to init connection to Database, as well as execute Queries"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.event_loop = asyncio.get_event_loop()
        self.conn_pool = None
        self.connected = False

    def cog_unload(self):
        self.logger.info("Closing Hemlock DB Connection")
        self.conn_pool.close()
        yield from self.conn_pool.wait_closed()
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        await self.connect_pool(
            host = self.config.h_db_host,
            user = self.config.h_db_user,
            password = self.config.h_db_pass,
            port = self.config.h_db_port,
            db = self.config.h_db_name,
            charset = 'utf8mb4',
            loop = self.event_loop,
            autocommit=True
        )

    async def execute_query(self, query, params):
        try:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
                    return await cur.fetchall()
        except Exception as e:
            self.logger.exception(f"Exception {e} while executing query {query}")

    async def connect_pool(self, **kwargs):
        if self.conn_pool is None:
            try:
                self.conn_pool = await aiomysql.create_pool(**kwargs)
                self.logger.info("Conenected to Hemlock Database")
                self.connected = True
            except BaseException as conn_exception:
                self.logger.error(f"Error {conn_exception} while connecting to hemlock database")
                self.logger.error("Disconnecing bot")
                self.connected = False
                await self.bot.logout()

def setup(bot):
    bot.add_cog(hemlock_db(bot))
