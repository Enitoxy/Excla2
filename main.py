"""
main.py
---
Author: Enitoxy
Co-authors: [empty]
License: GPL-3.0
Created: 2025-03-04
Description: The main file, aka entry point
"""

import asyncio
import os

from bot import Bot

TOKEN = os.environ["TOKEN"]


async def main():
    bot = Bot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
