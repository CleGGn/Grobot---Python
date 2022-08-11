import discord
from discord.ext import commands
from blagues_api import *
import asyncio

class BlaguesCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.blagues = BlaguesAPI("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTE0ODQ1MzYzMjM0NDA2NDAiLCJsaW1pdCI6MTAwLCJrZXkiOiJKTHk4UWpmbHQ5VnQ1b2ppR2VRUkRRTzQ0NHdYVUd1RzR2RkIzSkV4VFdjeGlvMExuYSIsImNyZWF0ZWRfYXQiOiIyMDIyLTA4LTExVDA4OjQ0OjI1KzAwOjAwIiwiaWF0IjoxNjYwMjA3NDY1fQ.4BttynRZaqryYjEbLcyAj7rCwE5wYnr_5yCqhY1kDOA")


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ FONCTIONS --------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ COMMANDS ---------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    @commands.command(
        name="blague",
        help="Raconte une blague hilarante"
    )
    async def blague(self, ctx):
        full_joke = await self.blagues.random()
        joke = full_joke.joke
        answer =  full_joke.answer
        await ctx.channel.send(joke)
        await asyncio.sleep(3)
        await ctx.channel.send("🎉 " + answer)

