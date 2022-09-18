import logging

import discord
import iniconfig

# Imported for initialisation
from configs.logs import config
import cleaning_cog


ini = iniconfig.IniConfig(".env")
TOKEN = ini["tokens"]["PROD"]

logger = logging.getLogger('main')

bot = discord.Bot()
bot.load_extension('cleaning_cog')

@bot.event
async def on_ready():
    logger.info(f"{bot.user} is ready and online!")

if __name__ == '__main__':
    bot.run(TOKEN)