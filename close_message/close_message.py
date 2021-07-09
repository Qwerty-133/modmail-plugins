from discord.ext import commands

from core import checks
from core import time
from core.models import PermissionLevel

DEFAULT_MESSAGE = "Feel free to open a new thread if you need anything else."


class UserFriendlyTimeOnly(time.UserFriendlyTime):
    async def convert(self, ctx, argument):
        converted = await super().convert(ctx, argument)
        if converted.arg:
            raise commands.BadArgument('A message cannot be supplied.')
        converted.arg = DEFAULT_MESSAGE
        return converted


class CloseMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='closemessage', aliases=['cm'], usage="[after]")
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def close_message(self, ctx, *, after: UserFriendlyTimeOnly = None):
        """Close the current thread with the default message."""
        return await self.bot.get_command('close')(ctx, after=after)


def setup(bot):
    bot.add_cog(CloseMessage(bot))
