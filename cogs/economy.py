"""
cogs.economy.py
---
Author: Enitoxy
Co-authors: [empty]
License: GPL-3.0
Created: 2025-03-04
Description: A cog/module containing economy commands (fishing)
"""

import random

from discord import Embed, Interaction, app_commands
from discord.ext import commands

from cogs.data.fish import fishes


class Economy(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    async def get_fish(self):
        while True:
            random_fish = random.choice(list(fishes))
            fish_chance = fishes[random_fish]["chance"]
            user_chance = random.uniform(0, 1)

            if user_chance <= fish_chance:
                return random_fish

    async def get_emoji(self, fish: str):
        if fish not in fishes:
            return None

        emoji_id = fishes[fish]["emoji_id"]
        if emoji_id is None:
            return f":{fish}:"
        else:
            return f"<:{fish}:{emoji_id}>"

    @app_commands.command(name="fish")
    async def fish(self, interaction: Interaction):
        fish = await self.get_fish()
        fish_name = fishes[fish]["name"]
        fish_value = fishes[fish]["value"]

        # Database entry before the embed

        emoji = await self.get_emoji(fish)

        embed = Embed(title="Fishin' time!", description="")
        embed.add_field(name="You caught:", value=fish_name)
        embed.add_field(name=emoji, value="")
        embed.add_field(name=f"Value: {fish_value}", value="", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Economy(bot))
