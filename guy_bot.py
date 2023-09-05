import logging
from typing import Mapping, Type
from discord.ext import commands
import os
from dotenv import load_dotenv
from asyncpg import Pool

load_dotenv()


class BaseConfig:
    TOKEN: str = os.getenv("TOKEN")
    DB_CONN_STR: str = os.getenv("DB_CONN_STR")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class Bot(commands.Bot):
    def __init__(self, config: Type[BaseConfig], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.pool: Pool = None

    @property
    def cogs(self) -> Mapping[str, "Cog"]:
        return super().cogs


class Cog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)

    async def cog_load(self) -> None:
        # log that cog is loaded
        self.logger.log(logging.INFO, f"Loaded cog {self.__class__.__name__}.")

    async def cog_unload(self) -> None:
        # log that cog is unloaded
        self.logger.log(logging.INFO, f"Unloaded cog {self.__class__.__name__}.")
