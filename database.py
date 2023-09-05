from typing import TYPE_CHECKING, TypeVar

import asyncpg
import discord

if TYPE_CHECKING:
    from asyncpg import Connection

S = TypeVar("S")


async def join_message_enabled(cursor: "Connection", guild: discord.Guild, setting: str) -> bool:
    v = await cursor.fetchrow(
        "SELECT join_message_enabled FROM guild_settings WHERE guild_id = $1 AND setting = $2",
        guild.id, setting
    )

    if not v:
        return None

    return v[0]
