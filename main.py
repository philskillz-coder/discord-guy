import logging

import asyncpg
import discord

import guy_bot
import asyncio
import argparse

discord.utils.setup_logging()

parser = argparse.ArgumentParser()
parser.add_argument("--dev", action="store_true")

args = parser.parse_args()
IS_DEVELOPMENT = args.dev


class Bot(guy_bot.Bot):
    INITIAL_COGS = [
        "cogs.main",
        "cogs.events"
    ]

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}.")

    async def setup_hook(self) -> None:
        self.pool = await asyncpg.create_pool(dsn=self.config.DB_CONN_STR, min_size=3, max_size=10)
        for cog in self.INITIAL_COGS:
            self.logger.log(logging.INFO, f"Loading extension {cog}.")
            await self.load_extension(cog)


async def main():
    if IS_DEVELOPMENT:
        config = guy_bot.DevelopmentConfig
    else:
        config = guy_bot.ProductionConfig

    intents = discord.Intents.default()
    intents.members = True
    async with Bot(config, command_prefix="!", intents=intents) as bot:
        await bot.start(bot.config.TOKEN)


asyncio.run(main())
