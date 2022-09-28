import logging

import iniconfig

import discord

# Imported for initialisation
import cleaning_cog  # noqa: F401
from configs.logs import config  # noqa: F401


ini = iniconfig.IniConfig("tokens.env")
TOKEN = ini["tokens"]["PROD"]

logger = logging.getLogger("main")

bot = discord.Bot()
bot.load_extension("cleaning_cog")

@bot.event
async def on_ready():
    logger.info(f"{bot.user} is ready and online!")

if __name__ == "__main__":
    bot.run(TOKEN)
