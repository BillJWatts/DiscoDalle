#!/usr/bin/env python
"""Entry point for the discord bot"""
import asyncio
import logging
import os
from pathlib import Path

import discord
import nest_asyncio
from discord.ext import commands

from logger_config import set_logging_config

COGS_PATH = Path("src/cogs")
DISCORD_API_TOKEN = os.getenv("DD_DISCORD_API_TOKEN")
COMMAND_PREFIX = "dd."


async def main():
    set_logging_config()
    bot = _create_bot()

    @bot.event
    async def on_ready():
        logging.info(f"Succesfully logged in as {bot.user}")

    await _load_cogs(bot)

    bot.run(DISCORD_API_TOKEN)


async def _load_cogs(bot: commands.Bot):
    """Loads all cogs present in the cogs directory"""

    await bot.load_extension("cogs.dalle_commands")


def _create_bot() -> commands.Bot:
    """Creates discord bot with message_content event subscription

    Returns:
        commands.Bot: Discord bot
    """
    # Intents are event subscriptions, we only need to monitor message events for this bot
    intents = discord.Intents.default()
    intents.message_content = True

    return commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


# discord.py 2.0 requires the bot to be run inside ascynio's asynchronous event loop.
# However asyncio may already be running due to other uses
# such as Jupyter notebooks, blocking asyncio.run().
# nest_asyncio allows the creation of nested event loops XXX is there a better way?
nest_asyncio.apply()
asyncio.run(main())
