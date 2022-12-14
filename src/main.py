import logging

import discord
import iniconfig

# Imported for initialisation
import cleaning_cog  # noqa: F401  # pylint: disable=unused-import
import cat_cog  # noqa: F401  # pylint: disable=unused-import
import configs.logs  # noqa: F401  # pylint: disable=unused-import

ini = iniconfig.IniConfig("tokens.env")
TOKEN = ini["tokens"]["PROD"]

logger = logging.getLogger("main")

bot = discord.Bot()  # type: ignore
bot.load_extension("cleaning_cog")
bot.load_extension("cat_cog")


@bot.event
async def on_ready() -> None:
    logger.info("%s is ready and online!", bot.user)


if __name__ == "__main__":
    bot.run(TOKEN)
