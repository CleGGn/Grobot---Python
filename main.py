import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
from ressources.anime import random_anime_digger, search_anime
import youtube_dl
from ressources.YTDLSource import YTDLSource

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Connecté en tant que {0.user}'.format(bot))

async def get_prefix(bot, message):
    default_prefix= '!'
    return default_prefix

@bot.command(
	brief="Writes pong"
)
async def ping(ctx):
	await ctx.channel.send("pong")

# Jikan Part
@bot.command(
    brief= "Fetch a random anime on MyAnimeList"
)
async def randanime(ctx):
    response = random_anime_digger()
    await ctx.channel.send(response)

@bot.command()
async def lfanime(ctx, *args):
	response = search_anime(args)
	await ctx.channel.send(response)

# Youtube Part
@bot.command(
    name='join', help='Appelle le bot dans le canal vocal'
    )
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} n'est pas connecté à un canal vocal".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(
    name='leave', help='Renvoie le bot du canal vocal'
    )
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Le bot n'est pas connecté à un canal vocal.")

@bot.command(
    name='play_song', help='To play song'
    )
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")        

@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]

    if message.content.lower() == "!hello":
        await message.channel.send(f'Coucou {username} ! UwU')
    elif message.content.lower() == '!bye':
        await message.channel.send(f'Au revoir {username} ^_^ !')
    elif message.content.lower()== '!random':
        response = f'Random number is : {random.randrange(1000000)}'
        await message.channel.send(response)

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)