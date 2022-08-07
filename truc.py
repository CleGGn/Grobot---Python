from re import I
import discord
import os
from dotenv import load_dotenv
import random
from jikanpy import Jikan
from pprint import pprint

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
jikan = Jikan()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel =str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'général':
        if user_message.lower() == 'hello':
            await message.channel.send(f'Coucou {username} ! UwU')
            return
        elif user_message.lower() == 'bye':
            await message.channel.send(f'Au revoir {username} ^_^ !')
            return
        elif user_message.lower()== '!random':
            response = f'Random number is : {random.randrange(1000000)}'
            await message.channel.send(response)
            return
        elif user_message.lower()== '!randanime':
            rdm_id = random.randrange(1,15251)
            anime = jikan.anime(rdm_id)
            titre_anime = anime['title']
            response = f'Ton anime aléatoire est : {titre_anime}'
            await message.channel.send(response)
            return

    if user_message.lower() == '!anywhere':
        await message.channel.send('Je suis partout')
        return
    

client.run(DISCORD_TOKEN)