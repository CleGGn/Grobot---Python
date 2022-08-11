import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class MusicCog(commands.Cog):
    def __init__(self,bot):
            self.bot = bot # Le BOT
            self.is_playing = False # Actuellement entrain de jouer de la musique ?
            self.is_paused = False # Actuellement en pause ?
            self.music_queue = [] # La file d'attente

            # Les options de FFMPEG
            self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

            # La musique en cours
            self.vc = None

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ FONCTIONS --------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Fonction qui va chercher la musique correspondante au lien
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0] # On utilise l'item donné et on retourne la source et le titre
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    # Fonction qui va servir à supprimer la musique en cours pour passer à celle d'après
    def play_next(self):
            # Si la liste d'attente est supérieur à 0
            if len(self.music_queue) > 0:
                # Alors on va passer à le premier élement de la liste
                self.is_playing = True 
                # On récupère la première élément de la liste dans une variable
                m_url = self.music_queue[0][0]['source']
                # On l'éjècte de la file d'attente
                self.music_queue.pop(0)
                # Et on le passe avec les options FFMPED.
                # à la fin de la chanson on  va rappeler la fonction play_next tant que la file d'attente n'est pas égale à 0
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

            # Sinon on arrête la musique en cours    
            else:
                self.is_playing = False

    # Fonction appelée quand on donne la commande play
    async def play_music(self, ctx):
        # Si la liste d'attente est supérieur à 0
        if len(self.music_queue) > 0:
            # Alors on va passer à le premier élement de la liste
            self.is_playing = True
            # On récupère la première élément de la liste dans une variable
            m_url = self.music_queue[0][0]['source']
            
            # Si le bot n'est pas connecté à un channel vocal, on le connecte à un channel vocal
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("J'ai pas reussi à me connecter")
                    return
            else:
                # Si le bot est connecté à un autre channel vocal, on le déplace dans celui où l'utilisateur est
                await self.vc.move_to(self.music_queue[0][1])
            
            # On l'éjècte de la file d'attente
            self.music_queue.pop(0)
            # Et on le passe avec les options FFMPED.
            # à la fin de la chanson on  va rappeler la fonction play_next tant que la file d'attente n'est pas égale à 0
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            # Sinon on arrête la musique en cours  
            self.is_playing = False

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------ COMMANDS ---------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    @commands.command(
        name="play", 
        aliases=["p","playing"], 
        help="Joue la musique correspondante à l'URL"
        )
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel  # le channel de l'utilisateur
        # Vérifie que l'utilisateur est connecté 
        if voice_channel is None:
            await ctx.send("T'as pas connecté à un canal zebi ! 😐 ")
        # Vérifie si la musique est en pause ou non
        elif self.is_paused:
            self.vc.resume()
        # Si elle ne l'est pas, on utilise notre fonction search_yt avec notre query
        else:
            song = self.search_yt(query)
            #Si le format de ce que nous retourne la fonction n'est pas le bon
            if type(song) == type(True):
                await ctx.send("J'ai pas reussi à récupérer la chanson, le format n'est pas le bon. \nJe ne peux pas lire les playlists ni les livestreams. 😑")
            # Sinon on l'ajoute à la file d'attente
            else:
                await ctx.send(f"Ajouté à la file d'attente : {song['title']} 😎")
                self.music_queue.append([song, voice_channel])
                # Si plus rien n'est entrain de jouer, on lance la première de la file d'attente avec la fonction play_music
                if self.is_playing == False:
                    await self.play_music(ctx)


    @commands.command(
        name="pause", 
        help="Met en pause la musique en cours"
        )
    async def pause(self, ctx, *args):
        # Si c'est entrain de jouer, on met en pause
        if self.is_playing: 
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        # Si c'est déja en pause, on relance
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(
        name = "resume", 
        aliases=["r"], 
        help="Relance la musique"
        )
    async def resume(self, ctx, *args):
        # Si c'est déja en pause, on relance
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(
        name="skip", 
        aliases=["s"], 
        help="Passe la chanson en cours et lance la prochaine"
        )
    async def skip(self, ctx):
        # Si une musique est entrain de jouer en ce moment
        if self.vc != None and self.vc:
            # On stop
            self.vc.stop()
            # On essaie de jouer la première musique de la file d'attente
            await self.play_music(ctx)


    @commands.command(
        name="queue", 
        aliases=["q"], 
        help="Affiche la file d'attente"
        )
    async def queue(self, ctx):
        queue = ""
        for i in range(0, len(self.music_queue)):
            # Montre les 5 premères chansons de la Q
            if (i > 4): break
            # On ajoute les titres à notre variable queue
            queue += self.music_queue[i][0]['title'] + "\n"
        # Si notre queue n'est pas vide, on l'affiche
        if queue != "":
            await ctx.send(queue)
        # Sinon on montre un message
        else:
            await ctx.send("C'est tout vide là dedans 😥")

    @commands.command(
        name="clear", 
        aliases=["c", "bin"], 
        help="Arrête la musique et nettoie la file d'attente"
        )
    async def clear(self, ctx):
        # Si quelque chose est entrain de jouer, on l'arrête
        if self.vc != None and self.is_playing:
            self.vc.stop()
        # On remet la file d'attente à zero    
        self.music_queue = []
        await ctx.send("C'est nettoyé, chef 🎈")

    @commands.command(name="leave",
        aliases=["disconnect", "l", "d"], 
        help="Renvoi le bot"
        )
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()