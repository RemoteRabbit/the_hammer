import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType


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

    @commands.command(name='bugs', aliases=['bug'])
    @cooldown(1, 10, BucketType.guild)
    async def bug_report(self, ctx, *, message):

        if len(message) > 20:
            bugs_channel1 = discord.utils.get(
                self.bot.get_all_channels(), guild__name='Westist', name='bugs')
            bugs_channel2 = discord.utils.get(
                self.bot.get_all_channels(), guild__name='Westist', name='bugs')
            embed = discord.Embed(
                title='BUG REPORTED',
                colour=0x008000
            )
            embed.add_field(name='Username', value=ctx.message.author)
            embed.add_field(name='User id', value=ctx.message.author.id)
            embed.add_field(name='Bug: ', value=message)

            if bugs_channel1 is not None:
                await bugs_channel1.send(embed=embed)
            elif bugs_channel2 is not None:
                await bugs_channel2.send(embed=embed)
            await ctx.send("Your bug has been reported")
        else:
            await ctx.send("Please enter your bug in more than 20 words, try describing everything\nOr you might have forgotten to use the quotes")

    @bug_report.error
    async def bug_report_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please enter the bug to be reported')
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.send("You didnt close the quotes!")
        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            await ctx.send("Too many quotes!")
        elif isinstance(error, commands.UnexpectedQuoteError):
            await ctx.send("Unexpected quote in non-quoted string")
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to CABREX')
            raise error


def setup(bot):
    bot.add_cog(Dev(bot))
