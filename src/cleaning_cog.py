import logging

from discord import ApplicationContext, Bot, Cog, slash_command, Interaction, TextChannel
from discord.ext import tasks


logger = logging.getLogger(__name__)

class Cleaning(Cog):

    def __init__(self, bot):
        self.bot = bot
        self._channels: list[TextChannel] = []
        self.clean.start()

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, channel):
        self._channels.append(channel)

    @slash_command()
    async def keep_clean(
        self, 
        ctx: ApplicationContext,
        ):
        '''Удаляет все сообщения старше одного дня'''
        assert isinstance(ctx.channel, TextChannel)
        logger.info('Channel "%s" saved for cleaning', ctx.channel.name)

        response = await ctx.respond(f'Оке, удаляю всё старше одного дня')
        assert isinstance(response, Interaction)
        await response.delete_original_message(delay=5)

    @tasks.loop(hours=24)
    async def clean(self):
        for channel in self.channels:
            logger.info('Cleaning channel "%s"', channel.name)
            await channel.purge()

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