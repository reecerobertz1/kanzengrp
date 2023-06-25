from bot import LalisaBot
import asyncio
import logging
import logging.handlers
from config import token

async def main():
    # this makes it so that whenever an error occurs  etc it sends
    # error messages in a file called discord.log instead
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=3,  # Rotate through 3 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # starts the bot
    async with LalisaBot() as bot:
        await bot.start(token) # token is imported at the top

asyncio.run(main())