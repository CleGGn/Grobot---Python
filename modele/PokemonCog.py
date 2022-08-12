from pydoc import resolve
import discord
import pokebase as pb
from discord.ext import commands
import pprint as pprint

import matplotlib.pyplot as plt
import numpy as np
plt.rcdefaults()

class PokemonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ax = plt.subplots()
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
            types_L = ""

            for type in types:
                truc = type.type
                truc2 = truc.name
                types_L += truc2.capitalize() + " "

            stats = entry.stats
            stats_L = []
            for stat in stats:
                truc = stat.base_stat
                stats_L.append(truc)
            embedVar = discord.Embed(title=name.capitalize(), color=0xFF0000)
            embedVar.add_field(name="Type", value=types_L, inline=False)
            embedVar.add_field(name="Height", value=height, inline=True)
            embedVar.add_field(name="Weight", value=weight, inline=True)
            embedVar.add_field(name="Stats", value=stats_L, inline=False)
            embedVar.set_image(url=image)
            return embedVar
        except AttributeError:
            dex += "Le pokemon est introuvable ou n'existe pas"
        return dex


    def truc(self, pokemon):
        people = ('PV', 'Attaque', 'Défense', 'Attaque spéciale', 'Défense spéciale', 'Vitesse')
        y_pos = np.arange(len(people))

        performance = 3 + 10 * np.random.rand(len(people))
        error = np.random.rand(len(people))

        self.ax.barh(y_pos, performance, xerr=error, align='center',
                color='yellow', ecolor='black')

        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(people)
        self.ax.invert_yaxis()  # labels read top-to-bottom
        self.ax.set_title('Statistiques')

        plt.show()

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
        embed.set_image(url="https://preview.redd.it/m5cl16t6alr21.jpg?auto=webp&s=23e1714a9e03860f413b68c0e55a06c78d74ed25")
        await ctx.channel.send(embed=embed)
