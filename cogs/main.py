import guy_bot
from discord import app_commands


class MainCog(guy_bot.Cog):
    pass


async def setup(bot: guy_bot.Bot) -> None:
    await bot.add_cog(MainCog(bot))
