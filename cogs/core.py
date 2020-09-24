import discord
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

        await self.bot.change_presence(activity=discord.Game('-'))


    @commands.command(description="Ping pong embeded command for testing connection")
    async def ping(self, ctx):
        """std ping pong command"""
        embed = discord.Embed(title=f":ping_pong: Pong! {round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed) 

    
def setup(bot):
    bot.add_cog(Core(bot))



        