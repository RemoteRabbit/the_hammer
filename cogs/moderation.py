import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description='Ban a given user with a reason (no reason given is `None`)')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(729886484966015029, 729887689867788379, 730647659299471382, 729888040876769320) #Role IDs in order literally.noam.chomsky, literally.server.admin, literally.moderator, and literally.bots
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """
        Ban a user for a given reason
        """
        await user.ban(reason=reason)
        embed = discord.Embed(title=f'Banned {user}\nReason: {reason}')
        await ctx.send(embed=embed)


    @commands.command(description='Clears a given number of messages within the current channel')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(729886484966015029, 729887689867788379, 730647659299471382, 729888040876769320) #Role IDs in order literally.noam.chomsky, literally.server.admin, literally.moderator, and literally.bots
    async def clear(self, ctx, amount:int):
        """
        Clears messages in current channel with given amount as an `int`
        """
        await ctx.channel.purge(limit=(amount+1))

    
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('dumb fuck Please send all required arguments. See `-help <command>` for more information.')


    @commands.group(description="The Hammer decides if a given member is cool or not")
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(729886484966015029, 729887689867788379, 730647659299471382, 729888040876769320) #Role IDs in order literally.noam.chomsky, literally.server.admin, literally.moderator, and literally.bots
    async def cool(self, ctx):
        """
        Says if a given user is cool.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


    @cool.command(name='bot')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(729886484966015029, 729887689867788379, 730647659299471382, 729888040876769320) #Role IDs in order literally.noam.chomsky, literally.server.admin, literally.moderator, and literally.bots
    async def _bot(self, ctx):
        """
        Is the bot cool?
        """
        await ctx.send('Yes, the bot is cool.')


    @commands.command(description='Kicks a given user with a reason (no reason given is `None`)')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(729886484966015029, 729887689867788379, 730647659299471382, 729888040876769320) #Role IDs in order literally.noam.chomsky, literally.server.admin, literally.moderator, and literally.bots
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """
        Kick a user for a given reason
        """
        await user.kick(reason=reason)


    @commands.command(description='Unban a given user')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(729886484966015029, 729887689867788379, 730647659299471382, 729888040876769320) #Role IDs in order literally.noam.chomsky, literally.server.admin, literally.moderator, and literally.bots
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



        