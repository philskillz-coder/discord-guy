import discord
import aiofiles
from aioEasyPillow import Editor, Canvas, Font, load_image
from io import BytesIO


async def generate_welcome_image(template: str, member: discord.Member) -> BytesIO:
    async with aiofiles.open(template, mode="rb") as f:
        picture = (await f.read()).decode()

    tmp = Editor(picture)
    profile_picture = Editor(await load_image(member.display_avatar.url))
    await profile_picture.circle_image()

    await tmp.paste(profile_picture, (0, 0))

    buf = BytesIO()
    await tmp.save(buf, "png")
    buf.seek(0)

    return buf
