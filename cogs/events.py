import os
from io import BytesIO
from typing import Optional, Tuple

import discord

import guy_bot
from discord.ext import commands
from discord import app_commands
import aiofiles
import aioEasyPillow

import image


class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


class EventsCog(guy_bot.Cog):
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        async with self.bot.pool.acquire() as conn:
            values: Tuple[bool, int, bool, str, bool, str] = await conn.fetchrow(
                "SELECT join_message_enabled, join_message_channel, join_text_enabled, join_text, join_picture_enabled, join_picture"
                "FROM guild_settings WHERE guild_id = $1",
                member.guild.id
            )
            join_message_enabled, join_message_channel, join_text_enabled, join_text, join_picture_enabled, join_picture = values

        if not join_message_enabled or (not join_text_enabled and not join_picture_enabled):
            return

        channel = member.guild.get_channel(join_message_channel)
        if channel is None:
            channel = await member.guild.fetch_channel(join_message_channel)

        if channel is None:
            return

        text = ""
        if join_message_enabled:
            text = join_text.format_map(FormatDict(
                member=member.name,
                menber_mention=member.mention,
                member_id=str(member.id),
                guild=member.guild.name,
                guild_id=str(member.guild.id)
            ))

        if not os.path.exists(join_picture):
            join_picture = "data/default_join_picture.png"

        async with aiofiles.open(join_picture, mode="rb") as f:
            picture = (await f.read()).decode()

        img: discord.File = None
        if join_picture_enabled:
            i = await image.generate_welcome_image(picture, member)
            img = discord.File(i, filename="welcome.png")
            i.close()

        await channel.send(text, file=img)


async def setup(bot: guy_bot.Bot) -> None:
    await bot.add_cog(EventsCog(bot))
