import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(description="The Hammer decides if a given member is cool or not")
    async def cool(self, ctx):
        """Says if a user is cool."""
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


    @cool.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')


    @commands.command(description='Clears a given number of messages within the current channel')
    async def clear(self, ctx, amount:int):
        """
        Clears messages in current channel with given amount as an `int`
        """
        await ctx.channel.purge(limit=(amount+1))


    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('dumb fuck Please send all required arguments. See `-help <command>` for more information.')


    @commands.command(description='Kicks a given user with a reason (no reason given is `None`)')
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """
        Kick a user for a given reason
        """
        await user.kick(reason=reason)


    @commands.command(description='Ban a given user with a reason (no reason given is `None`)')
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """
        ban a user for a given reason
        """
        await user.ban(reason=reason)
        embed = discord.Embed(title=f'Banned {user}\nReason: {reason}')
        await ctx.send(embed=embed)


    @commands.command(description='Unban a given user')
    async def unban(self, ctx, *, user):
        """
        Unban a given user
        """
        banned_users = await ctx.guild.bans()

        user_name, user_id = user.split('#')
        
        for ban_entry in banned_users:
            bUser = ban_entry.user

            if (bUser.name, bUser.discriminator) == (user_name, user_id):
                await ctx.guild.unban(bUser)
                embed = discord.Embed(title=f'Unbanned {bUser.name}#{bUser.discriminator}')
                await ctx.send(embed=embed)
                return

    
def setup(bot):
    bot.add_cog(Moderation(bot))



        