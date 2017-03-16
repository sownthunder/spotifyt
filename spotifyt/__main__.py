from __future__ import unicode_literals
from spotipy.oauth2 import SpotifyClientCredentials

import youtube_dl
import spotipy
import spotipy.util as util
import urllib.request
import urllib.parse
import re
import os

#Luastan's - Spotify -> Youtube -> download -> MP3.

os.system("clear")

#Spotify API credentials ("Client ID", "Client Secret")
#Aqui puedes conseguir tus credenciales: https://developer.spotify.com/my-applications
client_credentials_manager = SpotifyClientCredentials("", "")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#----------
#Busqueda del primer resultado de youtube dado un texto
def yt_search(canciones): #YT_VIDEO_ID = yt_search, cantidad("Lo que quieras encontrar en Youtube")
    z=[]
    for i in range(0,len(canciones)):
        print('\rBuscando cancion %s de %s' % (i+1, len(canciones)), sep=' ', end=15*' '+'\r', flush=True)
        texto=canciones[i]
        query_string = urllib.parse.urlencode({"search_query" : texto})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        enlasitos = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        z.append("https://www.youtube.com/watch?v=" + enlasitos[0]) #Devuelve la URL del video
    return z

print("############################")
print("# Luastan's Spotify -> MP3 #")
print("############################")
#------------Start
#Ejemplo_URI = 'spotify:user:luastan:playlist:1yd6b5BkiCO2k6ULHfqz8M'
uri = input('URI de tu lista de Spotify:\n')
username = uri.split(':')[2]
playlist_id = uri.split(':')[4]
print("############################\nAccion en progreso:")
print("Leyendo lista de Spotify.", sep=' ', end=15*' '+'\r', flush=True)
#----------- Saca la info de las canciones
def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks
#--------Song list humanizer
def humanizer_returnsx(resultados):
    L=[]
    tam = len(resultados)
    for i in range(0,tam):
        name = resultados[i]['track']['name']
        saltimbanquis=""
        for m in range(0,len(resultados[i]['track']['artists'])):
            saltimbanquis = saltimbanquis + " " + resultados[i]['track']['artists'][m]['name']
        L.append(name + saltimbanquis)
    print('\r -> Datos extraidos correctamente !', sep=' ', end=15*' '+'\r', flush=True)

    return L
#formato de la lista  ['song1 artist1 artist1a', 'song2 artist2', 'song3 artist 3']
spotify_list = humanizer_returnsx(get_playlist_tracks(username, playlist_id))
link_list = yt_search(spotify_list)
print('\r -> Busqueda completada !!', sep=' ', end=15*' '+'\r', flush=True)
ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'extract-audio': True,
    'audio-format': 'mp3',
    'quiet': True,
    'embed-thumbnail': True,
    'outtmpl': 'Descargas/'+'%(title)s.%(ext)s', #Carpeta de descarga por defecto esto es en la ruta donde ejecutas el programa/Descargas
    'postprocessors': [
        {'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'},
        {'key': 'EmbedThumbnail',},
    ]} #Estas opciones no me aclaraba con ellas no me juzgueis

def descargar(links):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for i in range(0, len(links)):
            print('\rDescargando cancion %s de %s' % (i+1, len(links)), sep=' ', end=15*' '+'\r', flush=True)
            ydl.download([links[i]])

descargar(link_list)
print("\r -> Descarga completada !!", sep=' ', end=15*' '+'\n', flush=True)
