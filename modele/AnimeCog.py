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
                return msg
            except jikanpy.JikanException:
                return msg
            except discord.DiscordException:
                return msg

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


    def random_manga_digger(self):
        check = True
        msg = "Wow! Je suis tombé sur une page qui n'existe plus ಠ_ಠ \nRelance la machine !!"
        while check == True:
            try:
                rdm_id = randrange(1,20850)
                manga = self.jikan.manga(rdm_id)
                trimmed_manga = self.manga_trimmer(manga)
                check = False
                return trimmed_manga
            except jikanpy.APIException:
                self.random_manga_digger()
            except jikanpy.JikanException:
                self.random_manga_digger()
            except discord.DiscordException:
                self.random_manga_digger()

    def manga_trimmer(self,manga):
        nl = '\n'
        manga_title = manga['title']
        manga_url = manga["url"]
        manga_score = manga["score"]
        manga_genre = manga['genres']
        manga_eng_title = manga['title_english']
        manga_genre_stock = ""

        if manga_eng_title != "None":
            eng_title = manga_eng_title

        for genre in manga_genre:
            if genre['name'] != "None":
                manga_genre_stock += "| " + genre['name'] + " | "
            else:
                manga_genre_stock = "Genre non précisé"    
        msg = f'{manga_title} / {eng_title}{nl}{nl}{manga_genre_stock}{nl}{nl}{manga_score} / 10{nl}{nl}{manga_url}'
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

            final_result =  list_results[:1]

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
        help="Affiche un anime aléatoire depuis MyAnimeList"
    )
    async def randanime(self, ctx):
        response = self.random_anime_digger()
        await ctx.channel.send(response)

    @commands.command(
        name="lfanime", 
        help="Recherche un anime"
    )
    async def lfanime(self,ctx, *args):
        response = self.search_anime(args)
        await ctx.channel.send(response)

    @commands.command(
        name="randmanga", 
        help="Affiche un manga aléatoire depuis MyAnimeList"
    )
    async def randmanga(self, ctx):
        response = self.random_manga_digger()
        print(response)
        await ctx.channel.send(response)
