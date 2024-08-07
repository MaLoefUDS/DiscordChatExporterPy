import datetime
import io
import traceback
from typing import List, Optional

from chat_exporter.construct.transcript import Transcript
from chat_exporter.ext.discord_import import discord
from chat_exporter.construct.attachment_handler import AttachmentHandler, AttachmentToLocalFileHostHandler, AttachmentToDiscordChannelHandler


async def quick_export(
    channel: discord.TextChannel,
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
):
    """
    Create a quick export of your Discord channel.
    This function will produce the transcript and post it back in to your channel.
    :param channel: discord.TextChannel
    :param guild: (optional) discord.Guild
    :param bot: (optional) discord.Client
    :return: discord.Message (posted transcript)
    """

    if guild:
        channel.guild = guild

    transcript = (
        await Transcript(
            channel=channel,
            limit=None,
            messages=None,
            pytz_timezone="UTC",
            military_time=True,
            fancy_times=True,
            before=None,
            after=None,
            support_dev=True,
            bot=bot,
            attachment_handler=None
            ).export()
        ).html

    if not transcript:
        return

    transcript_embed = discord.Embed(
        description=f"**Transcript Name:** transcript-{channel.name}\n\n",
        colour=discord.Colour.blurple()
    )

    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{channel.name}.html")
    return await channel.send(embed=transcript_embed, file=transcript_file)


async def export(
    channel: discord.TextChannel,
    limit: Optional[int] = None,
    tz_info="UTC",
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
    military_time: Optional[bool] = True,
    fancy_times: Optional[bool] = True,
    before: Optional[datetime.datetime] = None,
    after: Optional[datetime.datetime] = None,
    support_dev: Optional[bool] = True,
    attachment_handler: Optional[AttachmentHandler] = None,
):
    """
    Create a customised transcript of your Discord channel.
    This function will return the transcript which you can then turn in to a file to post wherever.
    :param channel: discord.TextChannel - channel to Export
    :param limit: (optional) integer - limit of messages to capture
    :param tz_info: (optional) TZ Database Name - set the timezone of your transcript
    :param guild: (optional) discord.Guild - solution for edpy
    :param bot: (optional) discord.Client - set getting member role colour
    :param military_time: (optional) boolean - set military time (24hour clock)
    :param fancy_times: (optional) boolean - set javascript around time display
    :param before: (optional) datetime.datetime - allows before time for history
    :param after: (optional) datetime.datetime - allows after time for history
    :param attachment_handler: (optional) attachment_handler.AttachmentHandler - allows custom asset handling
    :return: string - transcript file make up
    """
    if guild:
        channel.guild = guild

    return (
        await Transcript(
            channel=channel,
            limit=limit,
            messages=None,
            pytz_timezone=tz_info,
            military_time=military_time,
            fancy_times=fancy_times,
            before=before,
            after=after,
            support_dev=support_dev,
            bot=bot,
            attachment_handler=attachment_handler,
        ).export()
    ).html


async def raw_export(
    channel: discord.TextChannel,
    messages: List[discord.Message],
    tz_info="UTC",
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
    military_time: Optional[bool] = False,
    fancy_times: Optional[bool] = True,
    support_dev: Optional[bool] = True,
    attachment_handler: Optional[AttachmentHandler] = None,
):
    """
    Create a customised transcript with your own captured Discord messages
    This function will return the transcript which you can then turn in to a file to post wherever.
    :param channel: discord.TextChannel - channel to Export
    :param messages: List[discord.Message] - list of Discord messages to export
    :param tz_info: (optional) TZ Database Name - set the timezone of your transcript
    :param guild: (optional) discord.Guild - solution for edpy
    :param bot: (optional) discord.Client - set getting member role colour
    :param military_time: (optional) boolean - set military time (24hour clock)
    :param fancy_times: (optional) boolean - set javascript around time display
    :param attachment_handler: (optional) AttachmentHandler - allows custom asset handling
    :return: string - transcript file make up
    """
    if guild:
        channel.guild = guild

    return (
        await Transcript(
            channel=channel,
            limit=None,
            messages=messages,
            pytz_timezone=tz_info,
            military_time=military_time,
            fancy_times=fancy_times,
            before=None,
            after=None,
            support_dev=support_dev,
            bot=bot,
            attachment_handler=attachment_handler
        ).export()
    ).html


async def quick_link(
    channel: discord.TextChannel,
    message: discord.Message
):
    """
    Create a quick link for your transcript file.
    This function will return an embed with a link to view the transcript online.
    :param channel: discord.TextChannel
    :param message: discord.Message
    :return: discord.Message (posted link)
    """
    embed = discord.Embed(
        title="Transcript Link",
        description=(
            f"[Click here to view the transcript](https://mahto.id/chat-exporter?url={message.attachments[0].url})"
        ),
        colour=discord.Colour.blurple(),
    )

    return await channel.send(embed=embed)


async def quick_export(
    channel: str,
    guild: str = None,
    ticket_id: str = None,
    client: discord.Client = None,
):
    guild = client.get_guild(int(guild))
    channel = guild.get_channel(int(channel))

    # noinspection PyBroadException
    try:
        transcript = await Transcript.export(channel, None, "Europe/London")
    except Exception:
        traceback.print_exc()
        error_embed = discord.Embed(
            title="Transcript Generation Failed!",
            description="Whoops! We've stumbled in to an issue here.",
            colour=discord.Colour.red()
        )
        await channel.send(embed=error_embed)
        print(f"Please send a screenshot of the above error to https://www.github.com/mahtoid/DiscordChatExporterPy")
        return

    async for m in channel.history(limit=None):
        try:
            for f in m.attachments:
                if f"transcript-{channel.name}.html" in f.filename:
                    await m.delete()
        except TypeError:
            continue

    ticket_name = f"transcript-{channel.name}---{ticket_id}---.html"
    with open(f"/var/www/html/transcripts/{ticket_name}", "w") as f:
        f.write(transcript.html)

async def quick_export(
    channel: str,
    guild: str = None,
    ticket_id: str = None,
    client: discord.Client = None,
):
    guild = client.get_guild(int(guild))
    channel = guild.get_channel(int(channel))

    # noinspection PyBroadException
    try:
        transcript = await export(channel=channel, limit=10000, guild=guild)
    except Exception:
        traceback.print_exc()
        error_embed = discord.Embed(
            title="Transcript Generation Failed!",
            description="Whoops! We've stumbled in to an issue here.",
            colour=discord.Colour.red()
        )
        await channel.send(embed=error_embed)
        print(f"Please send a screenshot of the above error to https://www.github.com/mahtoid/DiscordChatExporterPy")
        return

    async for m in channel.history(limit=None):
        try:
            for f in m.attachments:
                if f"transcript-{channel.name}.html" in f.filename:
                    await m.delete()
        except TypeError:
            continue

    ticket_name = f"transcript-{channel.name}---{ticket_id}---.html"
    with open(f"/var/www/html/transcripts/{ticket_name}", "w") as f:
        f.write(transcript)

async def link(
    message: discord.Message
):
    """
    Returns a link which you can use to display in a message.
    This function will return a string of the link.
    :param message: discord.Message
    :return: string (link: https://mahto.id/chat-exporter?url=ATTACHMENT_URL)
    """
    return "https://mahto.id/chat-exporter?url=" + message.attachments[0].url
