import discord
from discord.ext import commands
import joke_api
import random

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))


    @commands.command(aliases=['8ball', 'eightball'], description='Will output a random 8 ball response provided a question <str>')
    async def _8ball(self, ctx, *, question):
        """
        Random 8ball response in response to question; Aliases: 8ball, eightball
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

    
def setup(bot):
    bot.add_cog(Other(bot))



        