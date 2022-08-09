from ast import Try
import jikanpy
from pprint import pp, pprint
from random import randrange, choice

jikan = jikanpy.Jikan()

def random_anime_digger():
    check = True
    array_msg = [
    "Wow! Je suis tombé sur une page qui n'existe plus, relance la machine bg !!", 
    "Hmmm non, ça n'a pas marché ( ͡° ͜ʖ ͡°)", 
    "Wola, je jure c'est pas ma faute si ça marche pas ಠ_ಠ"]
    while check == True:
        try:
            rdm_id = randrange(1,20850)
            anime = jikan.anime(rdm_id)
            trimmed_anime = anime_trimmer(anime)
            check = False
            return trimmed_anime
        except jikanpy.APIException:
            msg = choice(array_msg)
            return msg
        except jikanpy.JikanException:
            msg = choice(array_msg)
            return msg

def anime_trimmer(anime):
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


def search_anime(args):
    nl = '\n'
    list_results = []
    msg = "Les meilleurs résultats :" + nl

    search_results = jikan.search('anime', args)
    trimmed_results = search_results['results']

    for title in trimmed_results:
        search_row = title['title']
        list_results.append(search_row)

    final_result =  list_results[:10]

    for title in final_result:
        msg +=  title + nl   
    return (msg)
