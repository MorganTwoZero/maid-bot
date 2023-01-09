import datetime
import logging
import os

from discord import (
    ApplicationContext,
    Bot,
    Cog,
    Forbidden,
    Interaction,
    InvalidData,
    NotFound,
    TextChannel,
    slash_command,
)
from discord.ext import tasks  # type: ignore

from utils import file

logger = logging.getLogger(__name__)


class Cleaning(Cog):
    # init
    def __init__(self, bot: Bot):
        self.bot = bot
        self._channels: set[TextChannel] = set()
        self._file_name = "channels.txt"
        self.clean.start()  # pylint: disable=no-member

    @Cog.listener(name="on_connect")
    async def _load_channels(self) -> None:
        if os.path.exists(self._file_name):
            try:
                for channel_id in file.read_file(self._file_name):
                    channel_obj = await self.bot.fetch_channel(channel_id)
                    assert isinstance(channel_obj, TextChannel)
                    self._channels.add(channel_obj)
                    logger.debug("Loaded channel id %s from file", channel_id)
            except FileNotFoundError as e:
                logger.exception(e)
            except InvalidData as e:
                logger.exception(e)
            except NotFound as e:
                logger.exception(e)
            except Forbidden as e:
                logger.exception(e)

    # utils
    @tasks.loop(minutes=5)  # type: ignore
    async def clean(self) -> None:
        # TODO arbitrary ttl feature  # pylint: disable=fixme
        ttl = datetime.datetime.now() - datetime.timedelta(days=1)

        for channel in self._channels:
            res = await channel.purge(before=ttl)
            if len(res) > 0:
                logger.debug('Deleted %s messages in "%s"', len(res), channel.name)

    # commands
    @slash_command()  # type: ignore
    async def keep_clean(
        self,
        ctx: ApplicationContext,
    ) -> None:
        """Удаляет все сообщения старше одного дня."""
        if ctx.channel in self._channels:
            response = await ctx.respond("Я и так тут регулярно убираюсь!")
            assert isinstance(response, Interaction)
            await response.delete_original_message(delay=5)
            return

        try:
            assert isinstance(ctx.channel, TextChannel)

            self._channels.add(ctx.channel)
            file.save_channel_id(self._file_name, ctx.channel.id)
            logger.info('Channel "%s" saved for cleaning', ctx.channel.name)

            response = await ctx.respond("Оке, удаляю всё старше одного дня")
            assert isinstance(response, Interaction)
            await response.delete_original_message(delay=5)
        except FileNotFoundError as e:
            await ctx.respond(f"Ошибка! Детали: {e}")
        except InvalidData as e:
            await ctx.respond(f"Ошибка! Детали: {e}")
        except NotFound as e:
            await ctx.respond(f"Ошибка! Детали: {e}")
        except Forbidden as e:
            await ctx.respond(f"Ошибка! Детали: {e}")

    @slash_command(name="purge")  # type: ignore
    async def purge(self, ctx: ApplicationContext, limit: int) -> None:
        """Удаляет `limit` сообщений."""

        try:
            assert isinstance(ctx.channel, TextChannel)
            res = await ctx.channel.purge(limit=limit)
            logger.info('Deleted %s messages in "%s"', len(res), ctx.channel.name)

            response = await ctx.respond(f"Удалила {len(res)} сообщений")
            assert isinstance(response, Interaction)
            await response.delete_original_message(delay=5)
        except InvalidData as e:
            logger.exception(e)
        except NotFound as e:
            logger.exception(e)
        except Forbidden as e:
            logger.exception(e)


def setup(bot: Bot) -> None:
    bot.add_cog(Cleaning(bot))
