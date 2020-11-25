import logging
import os

import discord
from discord.ext import commands


description = 'This is the help stuff'
PREFIX = DEBUG = os.environ.get("PREFIX", default='h-')
bot = commands.Bot(command_prefix=PREFIX, description=description)


# Right now this is used for local dev, eventually make this part of the audit functionality
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(title=f':triangular_flag_on_post: Invalid command.', description=f'`-{ctx.invoked_with}` is not a command for The Hammer. Please refer to `-help` for more information.'))


# @bot.event
# async def on_member_join(ctx, user):
#     print(f'New user has doth joined! {user.name}')
#     try:
#         await ctx.send(embed=discord.Embed(title='New user', description='aaa'))
#     except:
#         print(f'Member not found {user.name}')


# Auto loads upon start of bot
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['BOT_KEY'])
