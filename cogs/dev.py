import discord
from discord.ext import commands


class Dev(commands.Cog):
    """
    Dev Cog!
    """

    def __init__(self, bot):
        self.bot = bot

    # Manual load cog command

    @commands.command(description='Manual command for loading cogs')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role('literally.bots', 'literally.dev')
    async def load(self, ctx, extension):
        """
        Manual command for loading cogs
        """
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Successfully loaded in `{extension}` cog!')

    # Manual unload cog command

    @commands.command(description='Manual command for unloading cogs')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role('literally.bots', 'literally.dev')
    async def unload(self, ctx, extension):
        """
        Manual command for unloading cogs
        """
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Successfully unloaded the `{extension}` cog!')


def setup(bot):
    bot.add_cog(Dev(bot))
