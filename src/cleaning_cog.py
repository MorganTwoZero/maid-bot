import datetime
import logging

from discord import ApplicationContext, Bot, Cog, slash_command, Interaction, TextChannel
from discord.ext import tasks


logger = logging.getLogger(__name__)

class Cleaning(Cog):

    def __init__(self, bot):
        self.bot = bot
        self._channels: set[TextChannel] = set()
        self.clean.start()

    @slash_command()
    async def keep_clean(
        self, 
        ctx: ApplicationContext,
        ):
        '''Удаляет все сообщения старше одного дня'''
        assert isinstance(ctx.channel, TextChannel)
        logger.info('Channel "%s" saved for cleaning', ctx.channel.name)

        self._channels.add(ctx.channel)

        response = await ctx.respond(f'Оке, удаляю всё старше одного дня')
        assert isinstance(response, Interaction)
        await response.delete_original_message(delay=5)

    @tasks.loop(minutes=5)
    async def clean(self):
        ttl = datetime.datetime.now() - datetime.timedelta(days=1)

        for channel in self._channels:
            res = await channel.purge(before=ttl)
            if len(res) != 0:
                logger.debug("Deleted %s messages", len(res))

    @slash_command(name='purge')
    async def purge(self, ctx: ApplicationContext, limit: int):
        '''Удаляет `limit` сообщений'''
        logger.info('Purging %s messages in "%s"', limit, ctx.channel)

        assert isinstance(ctx.channel, TextChannel)
        await ctx.channel.purge(limit=limit)

        response = await ctx.respond(f'Удалила {limit} сообщений')
        assert isinstance(response, Interaction)
        await response.delete_original_message(delay=5)

def setup(bot: Bot):
    bot.add_cog(Cleaning(bot))