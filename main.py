import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import modele.AnimeCog as anime
import modele.MusicCog as music
import modele.MusicCog as music
import modele.PokemonCog as pokemon
import modele.BlaguesCog as blague

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client.add_cog(music.MusicCog(client))
client.add_cog(anime.AnimeCog(client))
client.add_cog(blague.BlaguesCog(client))
client.add_cog(pokemon.PokemonCog(client))

async def get_prefix(client, message):
    default_prefix= '!'
    return default_prefix

@client.event
async def on_ready():
    print('Connecté en tant que {0.user}'.format(client))


@client.command(
	brief="Ecrit ping"
)
async def ping(ctx):
	await ctx.channel.send("pong")

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
    elif message.content.lower()== '!aram':
        response = "Oui"    
        await message.channel.send(response)

    await client.process_commands(message)

client.run(DISCORD_TOKEN)