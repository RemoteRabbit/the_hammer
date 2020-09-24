import discord
from discord.ext import commands

class All_Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Outputs when a given member joined server")
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


    
def setup(bot):
    bot.add_cog(All_Users(bot))



        