"""
cogs.economy.py
---
Author: Enitoxy
Co-authors: [empty]
License: GPL-3.0
Description: A cog/module containing economy commands (fishing)
"""

import random

from discord import Embed, Interaction, app_commands
from discord.ext import commands

from data.fish import fishes
from utils import db


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

    async def new_inventory(self, user_id: int):
        data = {
            "user_id": user_id,
            "bits": 0,
        }
        await db.inventory.insert_one(data)

    async def add_one_fish(self, interaction: Interaction, fish: str):
        query = {"user_id": interaction.user.id}
        user_inventory = await db.inventory.find_one(query)

        if user_inventory is None:
            await self.new_inventory(interaction.user.id)

        data = {"$inc": {fish: 1}}
        await db.inventory.update_one(query, data)

    @app_commands.command(name="fish")
    async def fish(self, interaction: Interaction):
        fish = await self.get_fish()
        fish_name = fishes[fish]["name"]
        fish_value = fishes[fish]["value"]

        await self.add_one_fish(interaction, fish)

        emoji = await self.get_emoji(fish)

        embed = Embed(title="Fishin' time!", description="")
        embed.add_field(name="You caught:", value=fish_name)
        embed.add_field(name=emoji, value="")
        embed.add_field(name=f"Value: {fish_value}", value="", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory")
    async def inventory(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        # This time, we'll use a filter because we only want to know about the items.
        query = {"user_id": interaction.user.id}
        _filter = {"_id": 0, "user_id": 0, "bits": 0}
        user_inventory = await db.inventory.find_one(query, _filter)

        if user_inventory is None:
            embed = Embed(
                title="You don't have anything in your inventory!",
                description="Try catching something with `/fish`!",
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = Embed(title="Your Inventory", description="")

        inventory_value = 0
        for item in user_inventory:
            if user_inventory[item] == 0:
                continue
            fish_name = fishes[item]["name"]
            fish_value = fishes[item]["value"]
            fish_amount = user_inventory[item]
            fish_emoji = await self.get_emoji(item)

            inventory_value += fish_amount * fish_value

            embed.add_field(
                name=f"{fish_name} {fish_emoji} x {fish_amount}",
                value=f"Single: {fish_value}, Total: {fish_amount*fish_value}",
                inline=False,
            )

        embed.set_footer(text=f"Total inventory value: {inventory_value}")
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Economy(bot))
