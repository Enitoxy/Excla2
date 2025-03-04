"""
bot.py
---
Author: Enitoxy
Co-authors: [empty]
License: GPL-3.0
Created: 2025-03-04
Description: File that contains the Bot class
"""

import os
import random

import discord
from discord.ext import commands, tasks

INTENTS = discord.Intents.all()
COMMAND_PREFIX = "/"


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=COMMAND_PREFIX, intents=INTENTS)

    async def on_ready(self): ...

    async def load_cogs(self):
        """Loads cogs from a specific directory"""
        for cog_file in os.listdir("./cogs"):
            await self.load_extension(f"cogs.{cog_file[:-3]}")

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

    # Set up and start tasks, load cogs, sync tree
    async def setup_hook(self):
        await self.start_tasks()
        await self.load_cogs()
        await self.tree.sync()
