"""
main.py
---
Author: Enitoxy
Co-authors: [empty]
License: GPL-3.0
Description: The main file, aka entry point
"""

import asyncio
import logging
import os
import random

import discord
from colorama import Fore
from discord.ext import commands, tasks

from app import server

TOKEN = os.environ["TOKEN"]
INTENTS = discord.Intents.all()
COMMAND_PREFIX = "/"

formatter = logging.Formatter(
    "{0}[%(asctime)s] {1}[%(levelname)s] {2}%(name)s {3}- %(message)s".format(
        Fore.GREEN,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.RESET,
    ),
    "%d-%m-%Y %H:%M:%S",
)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(handler)

log = logging.getLogger("main")


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=COMMAND_PREFIX, intents=INTENTS)

    async def on_ready(self):
        log.info("Excla! is online!")
        log.info(f"Latency: {round(self.latency, 4)}ms")
        log.info(f"Discord.py: {discord.__version__}")
        log.info(f"{len(self.guilds)} servers")

    async def load_cogs(self):
        """Loads cogs from a specific directory"""
        for cog_file in os.listdir("./cogs"):
            if cog_file.endswith(".py"):
                await self.load_extension(f"cogs.{cog_file[:-3]}")
                log.info(f"Loaded {cog_file}")

    @tasks.loop(minutes=2)
    async def status_task(self):
        """Changes the bot's status message every 2 minutes"""
        status_list = [
            "beep boop",
            "Supports slash commands!",
            "boop beep boop?",
            f"I'm in {len(self.guilds)} servers",
        ]
        status = random.choice(status_list)
        activity = discord.CustomActivity(name=status)
        await self.change_presence(activity=activity)

    @status_task.before_loop
    async def before_status_task(self):
        """Wait before starting the status task loop"""
        await self.wait_until_ready()

    async def start_tasks(self):
        """Starts the bot's tasks, each task set manually"""
        self.status_task.start()
        log.info("Started tasks")

    # Set up and start tasks, load cogs, sync tree
    async def setup_hook(self):
        await self.start_tasks()
        await self.load_cogs()
        await self.tree.sync()
        log.info("Synced tree")


async def main():
    bot = Bot()
    async with bot:
        bot_task = asyncio.create_task(bot.start(TOKEN))
        app_task = asyncio.create_task(server.serve())
        await asyncio.gather(bot_task, app_task)


if __name__ == "__main__":
    asyncio.run(main())
