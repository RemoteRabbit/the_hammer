import datetime
import os

import discord
import psycopg2
import sqlalchemy
from dateutil.relativedelta import relativedelta
from discord import Colour
from discord.ext import commands, tasks
from discord.utils import get
from sqlalchemy import Column, Integer, MetaData, String, Table, select
from sqlalchemy.pool import NullPool


council_roles = ['literally.noam.chomsky', 'literally.server.admin',
                 'literally.moderator', 'literally.bots', 'mod', 'operations']


def connect():
    """
    Function to connect to the tempbans table within the database
    """
    DATABASE_URL = os.environ['DATABASE_URL']
    try:
        conn = sqlalchemy.create_engine(DATABASE_URL, poolclass=NullPool)
        meta = sqlalchemy.MetaData(bind=conn,
                                   reflect=True)

        tempbans = Table('tempbans', meta, Column("id", Integer, primary_key=True),
                         autoload=True,
                         extend_existing=True)
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    return conn, meta, tempbans


def delete(user_id):
    """
    Function to delete a given row from 'tempbans' given user_id
    """
    conn, meta, tempbans = connect()
    query = tempbans.delete().where(tempbans.c.user_id == user_id)
    conn.execute(query)

    return


def insert(*args):
    """
    Function to insert the form data 'values' into table 'tempbans'
    """
    user_id, end_date, reason, user = args
    conn, meta, tempbans = connect()
    query = tempbans.insert().values(
        user_id=f'{user_id}',
        end_date=f'{end_date}',
        reason=f'{reason}',
        user=f'{user}')
    conn.execute(query)

    return


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_unmute.start()

    @tasks.loop(seconds=5.0)
    async def auto_unmute(self):
        """
        This function is on a loop that checks the database to see if one of the users in it has met their mute time requirement. If they have it kicks off the unmute process and removes that row from the database
        """
        try:
            conn, meta, tempbans = connect()
            s = select([tempbans])
            results = conn.execute(s)

            for row in results:
                current_date = datetime.datetime.now(datetime.timezone.utc)
                if row[2] <= current_date:
                    user_name = row[5]
                    print(
                        f'We got one! {user_name} can now be unbanned/unmuted. Processing...')
                    user_id = row[0]
                    user = get(self.bot.get_all_members(), id=user_id)
                    delete(user_id)
                    restricted_role = discord.utils.get(
                        user.guild.roles,
                        name="RESTRICTED")
                    await discord.Member.remove_roles(user, restricted_role)
                    message_channel = discord.utils.get(
                        self.bot.get_all_channels(), name='general')
                    await message_channel.send(embed=discord.Embed(
                        color=Colour.green(),
                        title=f'@{user_name} has been unmuted!',
                        description='*This action automatically done by The Hammer*'))
                    print(f'Unmute of {user_name} successful!')
                    return
        except Exception as e:
            print(f'Error connecting and pull data from database table {e}')

    @commands.command(description='Ban a given user with a reason (no reason given is `None`)')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(*council_roles)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """
        Ban a user for a given reason
        """
        await user.ban(reason=reason)
        await ctx.send(embed=discord.Embed(color=Colour.red(),
                                           title=f'@{user} has been Banned!',
                                           description=f'Banned {user}\nReason: {reason}'))

    @commands.command(description='Clears a given number of messages within the current channel')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(*council_roles)
    async def clear(self, ctx, amount: int):
        """
        Clears messages in current channel with given amount as an `int`
        """
        await ctx.channel.purge(limit=(amount+1))
        await ctx.send(embed=discord.Embed(color=Colour.blue(),
                                           title=f'{amount} messages cleared from #{ctx.channel.name} channel!'))

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Something looks to be wrong with your `-clear` command.')

    @commands.group(description="The Hammer decides if a given member is cool or not")
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(*council_roles)
    async def cool(self, ctx):
        """
        Says if a given user is cool.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

    @cool.command(name='bot')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(*council_roles)
    async def _bot(self, ctx):
        """
        Is the bot cool?
        """
        await ctx.send('Yes, the bot is cool.')

    @commands.command(description='Kicks a given user with a reason (no reason given is `None`)')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(*council_roles)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """
        Kick a user for a given reason
        """
        await ctx.send(embed=discord.Embed(color=Colour.red(),
                                           title='You literally got kicked!',
                                           description=f'@<{user}> has just been kicked.\nReason: {reason}'))
        await user.kick(reason=reason)

    @commands.command(description="Mutes a given user.")
    @commands.has_any_role(*council_roles)
    async def mute(self, ctx, user: discord.Member, reason=None):
        """
        Mutes a given user.
        """
        restricted_role = discord.utils.get(
            user.guild.roles, name="RESTRICTED")
        await ctx.send(embed=discord.Embed(color=Colour.red(),
                                           title=f'@{user} is Muted!',
                                           description=f'@{user} nickname "{user.nick}" is now being muted.\nReason: {reason}\nMuted by @{ctx.author.nick}'))
        await user.add_roles(restricted_role)
        message_channel = discord.utils.get(
            self.bot.get_all_channels(), name='bans-and-reasoning')
        await message_channel.send(embed=discord.Embed(color=Colour.red(),
                                                       title=f'@{user} is Muted!',
                                                       description=f'@{user} nickname "{user.nick}" is now being muted.\nReason: {reason}\nMuted by @{ctx.author.nick}'))

    @commands.command(description='Temp. Mute a given user over a given time; Y = years, M = Months, w = weeks, d = days, h = hours, and s = seconds \nExample: `-tempute @testaccount 1w example mute for one week`', pass_context=True)
    @commands.has_any_role(*council_roles)
    async def tempmute(self, ctx, user: discord.Member, duration, *, reason=None):
        """
        Command to temporarily mute a given user for given timeframe.
        """
        restricted_role = discord.utils.get(
            user.guild.roles, name="RESTRICTED")
        current_time = datetime.datetime.now(datetime.timezone.utc)

        d_sign = duration[-1:]
        d_time = int(duration[:-1])

        if d_sign == 'Y':
            end_date = current_time + relativedelta(years=d_time)
            d_term = 'Year(s)'
        elif d_sign == 'M':
            end_date = current_time + relativedelta(months=d_time)
            d_term = 'Month(s)'
        elif d_sign == 'w':
            end_date = current_time + relativedelta(weeks=d_time)
            d_term = 'Week(s)'
        elif d_sign == 'd':
            end_date = current_time + relativedelta(days=d_time)
            d_term = 'Day(s)'
        elif d_sign == 'h':
            end_date = current_time + relativedelta(hours=d_time)
            d_term = 'Hour(s)'
        elif d_sign == 'm':
            end_date = current_time + relativedelta(minutes=d_time)
            d_term = 'Minute(s)'
        elif d_sign == 's':
            end_date = current_time + relativedelta(seconds=d_time)
            d_term = 'Second(s)'
        else:
            await ctx.send('specify a time duration')
            return

        insert(user.id, end_date, reason, user)
        await ctx.send(embed=discord.Embed(color=Colour.red(),
                                           title=f'{user} has been Temp Muted',
                                           description=f'Reason: {reason}\nTimeline: {d_time} {d_term}\n*Operation initiated by @{ctx.author.nick}*'))
        await user.add_roles(restricted_role)
        bans_channel = discord.utils.get(
            self.bot.get_all_channels(), name='bans-and-reasoning')
        await bans_channel.send(embed=discord.Embed(color=Colour.red(),
                                                    title=f'{user} has been Temp Muted',
                                                    description=f'Reason: {reason}\nTimeline: {d_time} {d_term}\n*Operation initiated by @{ctx.author.nick}*'))

    @commands.command(description='Unban a given user')
    @commands.has_permissions(manage_messages=True)
    @commands.has_any_role(*council_roles)
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
                bans_channel = discord.utils.get(
                    self.bot.get_all_channels(), name='bans-and-reasoning')
                await bans_channel.send(embed=discord.Embed(color=Colour.green(),
                                                            title=f'Unbanned {bUser.name}#{bUser.discriminator}',
                                                            description=f'*Operation initiated by @{ctx.author.nick}*'))
                return

    @commands.command(description='Used to unmute a given user')
    @commands.has_any_role(*council_roles)
    async def unmute(self, ctx, user: discord.Member):
        """
        Used to unmute a given user.
        """
        restricted_role = discord.utils.get(
            user.guild.roles, name="RESTRICTED")

        conn, meta, tempbans = connect()
        s = select([tempbans])
        results = conn.execute(s)

        for result in results:
            if user.id == result[0]:
                print(
                    f'We got one! {user.name} will be removed from database. Proccessing...')
                delete(user.id)

        await ctx.send(embed=discord.Embed(color=Colour.green(),
                                           title=f'{user} has been unmuted!',
                                           description=f'*Operation initiated by @{ctx.author.nick}*'))
        await discord.Member.remove_roles(user, restricted_role)

        results.close()


def setup(bot):
    bot.add_cog(Moderation(bot))
