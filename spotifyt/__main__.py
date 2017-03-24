from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
from appJar import gui
from threading import Thread

import requests
import spotipy
import sys
import urllib.request
import urllib.parse
import re
import os
import time

import queue


import tkinter as tk

path = './Descargas/'
is_downloading = False


def hit_descarga(btn):
    root = tk.Tk()
    root.withdraw()
    uri = root.clipboard_get()
    #spotify:user:luastan:playlist:1eQDpeUFUe3LvxruExM53w
    if uri[:7] == 'spotify':
        path = app.directoryBox() + '/'
        print(path)
        status_downloading()
        lista_canciones = humanizer(get_playlist_tracks(uri))
        thread = Thread(target = progressive_downloader, args = (lista_canciones, path))
        thread.start()
        #progressive_downloader(lista_canciones,path)

    else:
        app.infoBox('Copia la direccion URI', 'Abre Spotify. En las opciones para compartir una playlist deberías encontrar la funcion: "Copiar URI de Spotify"')


def status_downloading():
    app.hideButton("Descargar !")
    app.showMeter("progress")

def status_patience():
    app.hideMeter("progress")
    app.showButton("Descargar !")



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
        conjunto = name + saltimbanquis
        conjunto = conjunto.replace("/",'')
        conjunto = conjunto.replace("\\",'')
        canciones.append(conjunto)
        #
    return canciones

def print_status(current, total):
    percentage = 100*current/total
    #app.setMeter("progress", percentage, text=str(percentage)[:5] + "%")
    app.setMeter("progress", percentage, str(current) + "/" + str(total))


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
    is_downloading = True
    for i in range(is_bbc):
        filename = path + song_names[i] + '.mp3'
        print_status(i, is_bbc)
        if not os.path.isfile(filename):
            downloader([song_names[i]], yt_in_mp3_generator([song_names[i]]), path) #In older versions i used to do this in 2 steps
            statinfo = os.stat(filename)
            #random im not a direct link anymore bullshic bypass
            timeout = 0
            while statinfo.st_size < 1000000 and timeout < 10: #Sometimes youtubeinmp3 has the wonderfull idea of changing direct links to randomnn webpages
                #time.sleep(5)
                print('Redownloading: ' + song_names[i])
                os.remove(filename)
                timeout += 1
                downloader([song_names[i]], yt_in_mp3_generator([song_names[i]]), path) #In older versions i used to do this in 2 steps
                statinfo = os.stat(filename)
            if timeout == 10:
                os.remove(filename)
                print('No se pudo descargar: ' + song_names[i])
    status_patience()
    app.infoBox("Descarga completada !", "Se completó la descarga con éxito")

app = gui()
app.setIcon("icon.gif")
app.setResizable(canResize=False)
app.setTitle('Spotifyt - by Luastan')
app.setGuiPadding(0,0)
app.setFont(15, font="Oswald")
app.setBg('black')
app.addImage("title", "title_low.gif",0,0,2)
app.addMeter("progress",1,0,2)
app.hideMeter("progress")
app.setMeterBg("progress","black")
app.setMeterPadding("progress", 0, 0)
app.setMeterFill("progress", "purple")
app.setMeterFg("progress", "white")
app.addButton("Descargar !", hit_descarga, 1, 0)
app.setButtonBg("Descargar !", 'black')
app.setButtonSticky("Descargar !","both")
app.setButtonFg("Descargar !", "white")
app.go()


if __name__ ==" __main__":

    print('pene')
    azul = 1+1



#pan
