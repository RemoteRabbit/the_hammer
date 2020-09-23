import discord
from discord.ext import commands
import logging
import random
import joke_api

description = '''This is the help stuff'''
bot = commands.Bot(command_prefix='-', description=description)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(description="Just outputs a joke from the joke api.")
async def joke(ctx):
    """Replies with a random joke"""
    joke = joke_api.get_joke()
    print(joke)

    if joke == False:
        await ctx.send("Couldn't get joke from API. Try again later.")
    else:
        await ctx.send(joke['setup'] + '\n' + joke['punchline'])


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command(description="Outputs when a given member joined server")
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.group(description="The Hammer decides if a given member is cool or not")
async def cool(ctx):
    """Says if a user is cool."""
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


@bot.command(description="Ping pong embeded command for testing connection")
async def ping(ctx):
    """std ping pong command"""
    embed = discord.Embed(title="Pong! :ping_pong:")
    await ctx.send(embed=embed)

bot.run('NzU4NDA4MDIxNzkyOTE1NTA4.X2uggg.P6S9zYBVMVz8bvTj-0Ft787kNwQ')