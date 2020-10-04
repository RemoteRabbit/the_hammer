from datetime import datetime

import discord
from discord.ext import commands


council_roles = ['literally.noam.chomsky', 'literally.server.admin',
                 'literally.moderator', 'literally.bots', 'mod', 'operations']


class All_Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Just a quick printout to council to let you know it's alive and running correctly.
        """
        print(f'Logged in as {self.bot.user.name}')
        print(f'With the ID of {self.bot.user.id}')
        print('------')

        await self.bot.change_presence(activity=discord.Game('h-'))


    @commands.command(description='Howdy there from Shen Bapiro')
    async def howdy(self, ctx):
        """
        A good ol howdy from Shen Bapiro
        """
        await ctx.send(file=discord.File('./media/howdyben.png', filename='howdyben.png'))


    @commands.command(description="Outputs when a given user joined server")
    async def joined(self, ctx, user: discord.Member = None):
        """
        Says when a user joined.
        """
        if user is None:
            user = ctx.author

        MONTH = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
        user_joined = user.joined_at
        month = user_joined.strftime("%m")
        user_id = user.id

        if month[:1] == '0':
            refined_month = MONTH[int(month[1:])-1]

        await ctx.send(content=f'{user.mention} ({user.name}#{user.discriminator}) joined in {user_joined.strftime("%d")} {refined_month} {user_joined.strftime("%Y")} at {user_joined.strftime("%H:%M")} UTC')

    @commands.command(description="Ping pong embeded command for testing connection")
    async def ping(self, ctx):
        """std ping pong command"""
        await ctx.send(embed=discord.Embed(
            title=f":ping_pong: Pong! {round(self.bot.latency * 1000)}ms"))

    @commands.command(description='Checks a users roles to make sure they have gone through the role onboarding process.', pass_context=True)
    @commands.has_any_role(*council_roles)
    async def role_check(self, ctx):
        """
        Checks your roles to make sure you have added roles
        """
        user_roles = ctx.author.roles
        user = ctx.author

        if len(user_roles) <= 2:
            channels = self.bot.get_all_channels()
            for channel in channels:
                if channel.name == "roles":
                    roles_channel = channel.id
                elif channel.name == "rules":
                    rules_channel = channel.id

            await ctx.send(f'Please checkout <#{roles_channel}> and <#{rules_channel}>')
            newbie_role = discord.utils.get(user.guild.roles, name="newbie")
            await discord.Member.add_roles(user, newbie_role)
        else:
            await ctx.send(f'Congrats on filling out your roles. Welcome aboard and have fun!')
            member_role = discord.utils.get(
                user.guild.roles, name="literally.member")
            newbie_role = discord.utils.get(user.guild.roles, name="newbie")
            await discord.Member.add_roles(user, member_role)
            await discord.Member.remove_roles(user, newbie_role)

    @commands.command(description='Socialism is when the government does stuff!')
    async def socialism(self, ctx):
        """
        Socialism is when the government does stuff!
        """
        await ctx.send(file=discord.File('./media/wolff_socialism.mp4', filename='wolff_socialism.mp4'))


def setup(bot):
    bot.add_cog(All_Users(bot))
