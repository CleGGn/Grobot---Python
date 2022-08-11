import discord
from discord.ext import commands
from blagues_api import *
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
BLAGUE_TOKEN = os.getenv("BLAGUE_TOKEN")

class BlaguesCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.blagues = BlaguesAPI(BLAGUE_TOKEN)

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

