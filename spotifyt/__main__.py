from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

import requests
import spotipy
import sys
import urllib.request
import urllib.parse
import re
import os
import time

#Retieves data from spotify playlist given playlist id & user witch comes form uri
def get_playlist_tracks(uri):
    #Spotify api auth
    client_credentials_manager = SpotifyClientCredentials("", "")
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #Username and id
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]

    #Retrieve data from playlist
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']

    #THis loop is required to bypass 100 track per list limit
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

#get_playlist_id returns a big ass dictionary with a shit ton of unnecesary data
def humanizer(results):
    canciones=[] #List to save song names
    tam = len(results)
    for i in range(0,tam):
        name = results[i]['track']['name']
        saltimbanquis=""
        for m in range(0,len(results[i]['track']['artists'])):
            saltimbanquis = saltimbanquis + " " + results[i]['track']['artists'][m]['name']
        canciones.append(name + saltimbanquis)

        #
    return canciones

def print_status(current, total):
    print('\rDescargando cancion %s de %s' % (current, total), sep=' ', end=50*' '+'\r', flush=True)


#Searches stuff in youtube. Returns first search result in youtubeinmp3 direct link format
# WHy only first search result what if it is a music video¿??¿?¿?¿ - > Search Forbbiden voices MArtin Garrix
def yt_in_mp3_generator(canciones):
    links=[]
    for i in range(0,len(canciones)):
        texto=canciones[i]
        legit_links=[]
        query_string = urllib.parse.urlencode({"search_query" : texto})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        enlasitos = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        links.append("https://www.youtubeinmp3.com/fetch/?video=https://www.youtube.com/watch?v=" + enlasitos[0])

    return links


#FUnction name is self-explanatory
def downloader(song_names, links_youtubeinmp3, path):
    for i in range(len(song_names)):
        filename = path + song_names[i] + '.mp3'
        if not os.path.isfile(filename): #if not os.path.isfile(PATH + song_names[i] + '.mp3'):
            os.makedirs(os.path.dirname(filename), exist_ok = True)
            with urllib.request.urlopen(links_youtubeinmp3[i]) as data:
                with open(filename, "wb") as f:
                    f.write(data.read())



def progressive_downloader(song_names, path): #This function merges the link generator with the downloader.
    is_bbc = len(song_names)                  #I want to add a continue progress thing but mayb later
    for i in range(is_bbc):
        filename = path + song_names[i] + '.mp3'

        print_status(i + 1, is_bbc)

        if not os.path.isfile(filename):
            downloader([song_names[i]], yt_in_mp3_generator([song_names[i]]), path) #In older versions i used to do this in 2 steps
            statinfo = os.stat(filename)
            #random im not a direct link anymore bullshic bypass
            while statinfo.st_size < 1000000: #Sometimes youtubeinmp3 has the wonderfull idea of changing direct links to randomnn webpages
                os.remove(filename)
                downloader([song_names[i]], yt_in_mp3_generator([song_names[i]]), path) #In older versions i used to do this in 2 steps
                statinfo = os.stat(filename)


#www.youtubeinmp3.com/fetch/?video=https://www.youtube.com/watch?v=Zv1QV6lrc_Y
if __name__ == '__main__':
    #Actual program
    path = "./Descargas/"
    if len(sys.argv)>1:
        uri = sys.argv[1]
        if len(sys.argv)>2:
            path = sys.argv[2]
    else:
        uri = input('sportify URI_')
    #ista_canciones = humanizer(get_playlist_tracks(uri))
    progressive_downloader(lista_canciones, path)
    print('\n\n')
