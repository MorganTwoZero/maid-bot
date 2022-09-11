import logging
import os

import discord
from dotenv import load_dotenv

from configs.logs import config
import cleaning_cog

load_dotenv()

TOKEN = os.getenv("TOKEN")


logger = logging.getLogger('main')

bot = discord.Bot()
bot.load_extension('cleaning_cog')

@bot.event
async def on_ready():
    logger.info(f"{bot.user} is ready and online!")

if __name__ == '__main__':
    bot.run(TOKEN)