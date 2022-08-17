from pydoc import resolve
import discord
import pokebase as pb
import os
from discord.ext import commands
import pprint as pprint
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image  
import PIL  

plt.rcdefaults()

class PokemonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ FONCTIONS --------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def pokedex_catcher(self,pokemon):
        dex = ""
        entry = pb.pokemon(pokemon.lower())  
        try:
            id = entry.id
            name = entry.name
            height = entry.height
            weight = entry.weight
            sprite = pb.SpriteResource('pokemon', id)
            image = sprite.url
            types = entry.types
            stats_string = ""

            for type in types:
                type2 = type.type
                name_type = type2.name
                stats_string += name_type.capitalize() + " "

            stats = entry.stats
            stats_L = []
            nom_stats = []
            for stat in stats:
                stats2 = stat.base_stat
                statsname = stat.stat.name
                stats_L.append(stats2)
                nom_stats.append(statsname)

            self.plot(stats_L)

            embedVar = discord.Embed(title=name.capitalize() + " #" + str(id), color=0xFF0000)
            embedVar.add_field(name="Type", value=stats_string, inline=False)
            embedVar.add_field(name="Height", value=height, inline=True)
            embedVar.add_field(name="Weight", value=weight, inline=True)
            embedVar.set_thumbnail(url=image)
            return embedVar
        except AttributeError:
            dex += "Le pokemon est introuvable ou n'existe pas"
        return dex

    def plot(self,stats):
        COLOR = "white"
        plt.rcParams['text.color'] = COLOR
        plt.rcParams['axes.labelcolor'] = COLOR
        plt.rcParams['xtick.color'] = COLOR
        plt.rcParams['ytick.color'] = COLOR
        fig, ax = plt.subplots()
        
        langs = ['PV', 'Attaque', 'Défense','AttSpé', 'DéfSpé', 'Vitesse']
        y_pos = np.arange(len(langs))
        x_pos = [0, 50, 100, 150, 200, 255]

        ax.set_xticks(x_pos)
        ax.get_xaxis().set_visible(False)
        ax.set_yticks(y_pos, labels=langs)
        bar = ax.barh(langs, stats)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.set_xlim(0,255)  
        ax.bar_label(bar, label_type='center')
        ax.invert_yaxis()

        fig.savefig("stat.png",transparent=True)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ COMMANDS ---------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    @commands.command(
        name="pokemon",
        help="Recherche un pokemon"
    )
    async def pokemon(self, ctx, arg):
        embedVar = self.pokedex_catcher(arg)
        file = discord.File("stat.png", filename="image.png")
        embedVar.set_image(url="attachment://image.png")
        embedVar.set_footer(text="Demandé par : {}".format(ctx.author.display_name))
        await ctx.channel.send(file=file, embed=embedVar)

    @commands.command(        
        name="pokeballGO",
        aliases=["pokeballgo"],
        help="Lance une pokéball")
    async def pokeball(sel,ctx):
        embed = discord.Embed(title="Pokeball GO !") 
        embed.set_image(url="https://preview.redd.it/m5cl16t6alr21.jpg?auto=webp&s=23e1714a9e03860f413b68c0e55a06c78d74ed25")
        await ctx.channel.send(embed=embed)
