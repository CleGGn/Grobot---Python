import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
from modele.anime import random_anime_digger, search_anime
import modele.MusicCog as music


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

client.add_cog(music.MusicCog(client))

@client.event
async def on_ready():
    print('Connecté en tant que {0.user}'.format(client))

async def get_prefix(client, message):
    default_prefix= '!'
    return default_prefix

@client.command(
	brief="Writes pong"
)
async def ping(ctx):
	await ctx.channel.send("pong")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ Jikan Part ------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
@client.command(
    brief= "Fetch a random anime on MyAnimeList"
)
async def randanime(ctx):
    response = random_anime_digger()
    await ctx.channel.send(response)

@client.command()
async def lfanime(ctx, *args):
	response = search_anime(args)
	await ctx.channel.send(response)



@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]

    if message.content.lower() == "!hello":
        await message.channel.send(f'Coucou {username} ! UwU')
    elif message.content.lower() == '!bye':
        await message.channel.send(f'Au revoir {username} ^_^ !')
    elif message.content.lower()== '!random':
        response = f'Random number is : {random.randrange(1000000)}'
        await message.channel.send(response)

    await client.process_commands(message)

client.run(DISCORD_TOKEN)