import discord
from discord.ext import commands
import logging
import os


description = '''This is the help stuff'''
bot = commands.Bot(command_prefix='-', description=description)


# Right now this is used for local dev, eventually make this part of the audit functionality 
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Default invalid commad error message
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(title=f':triangular_flag_on_post: Invalid command.', description=f'`-{ctx.invoked_with}` is not a command for The Hammer. Please refer to `-help` for more information.'))


# Auto loads upon start of bot
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['BOT_KEY'])