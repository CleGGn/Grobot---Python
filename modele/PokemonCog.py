from pydoc import resolve
import discord
import pokebase as pb
import os
from discord.ext import commands
import pprint as pprint
import matplotlib.pyplot as plt
import numpy as np

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

            img_stats = self.plot(stats_L)

            embedVar = discord.Embed(title=name.capitalize() + " #" + str(id), color=0xFF0000)
            embedVar.add_field(name="Type", value=stats_string, inline=False)
            embedVar.add_field(name="Height", value=height, inline=True)
            embedVar.add_field(name="Weight", value=weight, inline=True)
            embedVar.add_field(name="Stats", value=nom_stats, inline=False)
            embedVar.add_field(name="Statssuite", value=stats_L, inline=False)
            embedVar.add_field(name="statsgraph",value=img_stats, inline=False)
            embedVar.set_image(url=image)
            return embedVar
        except AttributeError:
            dex += "Le pokemon est introuvable ou n'existe pas"
        return dex

    def plot(self,stats):
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1, ])
        langs = ['PV', 'Attaque', 'Défense','Attaque spéciale', 'Défense spéciale', 'Vitesse']
        students = [23, 17, 35, 29, 12, 6]
        ax.set_yticks(students)
        ax.barh(langs, students, align='center')
        ax.invert_yaxis()
        plt.savefig("stat.png")

    def create_pnj(self, imgstats):

        with open("stat.png", "xt") as f:
            f.write(imgstats)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ COMMANDS ---------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    @commands.command(
        name="pokemon",
        help="Recherche un pokemon"
    )
    async def pokemon(self, ctx, arg):
        embedVar = self.pokedex_catcher(arg)
        embedVar.set_footer(text="Demandé par : {}".format(ctx.author.display_name))
        await ctx.channel.send(embed=embedVar)

    @commands.command(        
        name="pokeballGO",
        aliases=["pokeballgo"],
        help="Lance une pokéball")
    async def pokeball(sel,ctx):
        embed = discord.Embed(title="Pokeball GO !") 
        color = 0x9b59b6
        embed.set_image(url="https://preview.redd.it/m5cl16t6alr21.jpg?auto=webp&s=23e1714a9e03860f413b68c0e55a06c78d74ed25")
        await ctx.channel.send(embed=embed)
