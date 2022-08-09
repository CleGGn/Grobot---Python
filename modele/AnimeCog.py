import discord
from discord.ext import commands
from ast import Try
import jikanpy
from pprint import pp, pprint
from random import randrange, choice

class AnimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jikan = jikanpy.Jikan()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ FONCTIONS --------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def random_anime_digger(self):
        check = True
        msg = "Wow! Je suis tombé sur une page qui n'existe plus ಠ_ಠ \nRelance la machine !!"
        while check == True:
            try:
                rdm_id = randrange(1,20850)
                anime = self.jikan.anime(rdm_id)
                trimmed_anime = self.anime_trimmer(anime)
                check = False
                return trimmed_anime
            except jikanpy.APIException:
                self.random_anime_digger()
            except jikanpy.JikanException:
                self.random_anime_digger()
            except discord.DiscordException:
                self.random_anime_digger()

    def anime_trimmer(self,anime):
        nl = '\n'
        anime_title = anime['title']
        anime_url = anime["url"]
        anime_score = anime["score"]
        anime_genre = anime['genres']
        anime_eng_title = anime['title_english']
        anime_genre_stock = ""

        if anime_eng_title != "None":
            eng_title = anime_eng_title

        for genre in anime_genre:
            if genre['name'] != "None":
                anime_genre_stock += "| " + genre['name'] + " | "
            else:
                anime_genre_stock = "Genre non précisé"    
        msg = f'{anime_title} / {eng_title}{nl}{nl}{anime_genre_stock}{nl}{nl}{anime_score} / 10{nl}{nl}{anime_url}'
        return msg


    def search_anime(self, args):
        nl = '\n'
        list_results = []
        msg = "Les meilleurs résultats :" + nl
        msgerror = "Un truc qui bug là"

        try:
            search_results = self.jikan.search('anime', args)
            trimmed_results = search_results['results']

            for title in trimmed_results:
                search_row = title['title'] + ", " + title['url']
                list_results.append(search_row)

            final_result =  list_results[:5]

            for title in final_result:
                msg +=  title + nl   
            return (msg)
        except jikanpy.APIException:
            return msgerror
        except jikanpy.JikanException:
            return msgerror
        except discord.DiscordException:
            return msgerror

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ COMMANDS ---------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #


    @commands.command(
        name="randanime", 
        help="Affiche un anime aléatoire depuis MYAnimeList"
    )
    async def randanime(self, ctx):
        response = self.random_anime_digger()
        print(response)
        await ctx.channel.send(response)

    @commands.command(
        name="lfanime", 
        help="Affiche les resultats de la recherche depuis MAL"
    )
    async def lfanime(self,ctx, *args):
        response = self.search_anime(args)
        await ctx.channel.send(response)