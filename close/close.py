from discord.ext import commands

from core import checks
from core import time
from core.models import PermissionLevel

DEFAULT_MESSAGE = "Feel free to open a new thread if you need anything else."


class UserFriendlyTimeOnly(time.UserFriendlyTime):
    async def convert(self, ctx, argument):
        converted = await super().convert(ctx, argument)
        if not converted.arg:
            converted.arg = DEFAULT_MESSAGE
        elif converted.arg not in ('silently', 'silently'):
            raise commands.BadArgument('A message cannot be supplied.')

        return converted


class CloseMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.close_command = self.bot.get_command('close')

    @commands.command(name='c', usage="[after]")
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def close(self, ctx, *, after='15m'):
        """Close the current thread with the default message."""
        after = await UserFriendlyTimeOnly().convert(ctx, after)
        return await self.close_command(ctx, after=after)

    @commands.command(name='cs', usage="[after]")
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def close_silently(self, ctx, *, after='15m'):
        """Close the current thread silently."""
        after = await UserFriendlyTimeOnly().convert(ctx, f'{after} silently')
        return await self.close_command(ctx, after=after)


def setup(bot):
    bot.add_cog(CloseMessage(bot))
