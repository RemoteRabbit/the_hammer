import random

import discord
from discord import Colour
import joke_api
from discord.ext import commands
from aiohttp import request


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command(name='8ball', aliases=['eightball'], description='Will output a random 8 ball response provided a question <str>')
    async def _8ball(self, ctx, *, question):
        """
        Random 8ball response in response to question
        """
        responses = ['It is certain',
                     'Without a doubt',
                     'You may rely on it',
                     'Yes definitely',
                     'It is decidedly so',
                     'As I see it, yes',
                     'Most likely',
                     'Yes',
                     'Outlook good',
                     'Signs point to yes',
                     'Reply hazy try again',
                     'Better not tell you now',
                     'Ask again later',
                     'Cannot predict now',
                     'Concentrate and ask again',
                     'Don\’t count on it',
                     'Outlook not so good',
                     'My sources say no',
                     'Very doubtful',
                     'My reply is no'
                     ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(description="Just outputs a joke from the joke api.")
    async def joke(self, ctx):
        """Replies with a random joke"""
        joke = joke_api.get_joke()

        if joke == False:
            await ctx.send("Couldn't get joke from API. Try again later.")
        else:
            await ctx.send(joke['setup'] + '\n' + joke['punchline'])

    @commands.command(description='')
    async def dog(self, ctx):
        api_url = "https://random.dog/woof.json"
        async with request("GET", api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data["url"]
                await ctx.send(embed=discord.Embed(color=Colour.green()).set_image(url=image_url))
            else:
                await ctx.send(f"The API seems down, says {response.status}")

    @dog.error
    async def dog_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback')
            raise error

    @commands.command(description='')
    async def cat(self, ctx):
        api_url = 'http://aws.random.cat/meow'
        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['file']
                await ctx.send(embed=discord.Embed(color=Colour.green()).set_image(url=image_url))
            else:
                await ctx.send(embed=discord.Embed(color=Colour.red(), title=f'Api is down', description=f'Response: {response.status}'))

    @cat.error
    async def cat_picture_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback')
            raise error


def setup(bot):
    bot.add_cog(Other(bot))
