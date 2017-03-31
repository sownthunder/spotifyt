#imports

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
import webbrowser

import tkinter as tk
import tkinter.simpledialog

#Global variables
path = ''
retry_songs = []
wrong_link = False

def is_updated():
    readme_gh = requests.get('http://raw.githubusercontent.com/luastan/spotifyt/master/README.md')
    if not readme_gh.text[53:59] == '0.6.05':
        if syt.okBox('New Version', "There's a new version available. Would you like to download it?"):
            webbrowser.open_new_tab('https://github.com/luastan/spotifyt/releases')
            sys.exit(0)
#spotify:user:luastan:playlist:2jcA2rX8MNpUtDQ5EX8nPw
def hit_descarga(btn):
    uri = 'notspotify:user:auser:aplaylist:code1eQDpeUFUe3LvxruExM53w'
    try:
        root = tk.Tk()
        root.withdraw()
        uri = root.clipboard_get()
    except:
        syt.infoBox('Copy the playlist link', 'Open Spotify and get the playlist link in the sharing options')
        return

    if uri[:29] == 'https://open.spotify.com/user' or uri[:13] == 'spotify:user:':
        path = syt.directoryBox() + '/'
        bypass_assholes = get_playlist_tracks(uri) #This is a quick fix keeping people from trying to download an invalid link

        if wrong_link:
            syt.infoBox('Copy the playlist link', 'Open Spotify and get the playlist link in the sharing options')
            return

        lista_canciones = humanizer(bypass_assholes)
        thread = Thread(target = progressive_downloader, args = (lista_canciones, path))
        thread.start()

    else:
        syt.infoBox('Copy the playlist link', 'Open Spotify and get the playlist link in the sharing options')

def status_downloading():
    syt.hideButton("Download !")
    syt.showMeter("progress")

def status_patience():
    syt.hideMeter("progress")
    syt.showButton("Download !")

#Retieves data from spotify playlist given playlist id & user witch comes form uri
def get_playlist_tracks(uri):
    #Spotify api auth
    client_credentials_manager = SpotifyClientCredentials("", "")
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #Username and id 2jcA2rX8MNpUtDQ5EX8nPw
    #spotify:user:luastan:playlist:2jcA2rX8MNpUtDQ5EX8nPw

    if uri[:29] == 'https://open.spotify.com/user':
        username = uri.split('/')[4]
    else:
        username = uri.split(':'[2])

    playlist_id = uri[-22:]
    wrong_link = False
    print(username)
    print(playlist_id)
    try:
        results = sp.user_playlist_tracks(username, playlist_id)
    except:
        wrong_link = True
        return []

        #Retrieve data from playlist
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
        conjunto = conjunto.replace('"','')
        conjunto = conjunto.replace("\\",'')
        conjunto = conjunto.replace("'",'')
        canciones.append(conjunto)
        #
    return canciones

def print_status(current, total):
    percentage = 100*current/total
    #syt.setMeter("progress", percentage, text=str(percentage)[:5] + "%")
    syt.setMeter("progress", percentage, str(current) + "/" + str(total))

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
        try:
            links.append("http://www.youtubeinmp3.com/fetch/?video=http://www.youtube.com/watch?v=" + enlasitos[0])
        except :
            links.append("http://www.youtubeinmp3.com/fetch/?video=http://www.youtube.com/watch?v=" + canciones[i].split(' ')[0])

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
    retry_songs = []
    retry_songs_number = 0
    status_downloading()
    is_bbc = len(song_names)                  #I want to add a continue progress thing but mayb later

    for i in range(is_bbc):
        filename = path + song_names[i] + '.mp3'
        print_status(i, is_bbc)
        try:
            if not os.path.isfile(filename):
                #print(song_names[i])
                downloader([song_names[i]], yt_in_mp3_generator([song_names[i]]), path) #In older vercsions i used to do this in 2 steps
                statinfo = os.stat(filename)
                #random im not a direct link anymore bullshic bypass
                retry = 0
                while statinfo.st_size < 1000000 and retry < 10: #Sometimes youtubeinmp3 has the wonderfull idea of changing direct links to randomnn webpages
                    #time.sleep(5)
                    print('Redownloading: ' + song_names[i])
                    os.remove(filename)
                    retry += 1
                    downloader([song_names[i]], yt_in_mp3_generator([song_names[i]]), path) #In older versions i used to do this in 2 steps
                    statinfo = os.stat(filename)
                if retry == 10:
                    os.remove(filename)
                    #Here  I want to store the lost songs name and their link to youtubeinmp3
                    retry_songs.append([song_names[i], yt_in_mp3_generator([song_names[i]])])
                    retry_songs_number+=1
        except:
            pass

    status_patience()

    if retry_songs_number == 0:
        syt.infoBox("Download completed !", "Download fully completed ! enjoy your music =) ")
    elif syt.yesNoBox("Download completed", "Spotifyt wasn't able to retrieve some songs from YoutubeInMp3. Would you like to save the rebel links in a file to download the music manually?"):
        text_recover_path = syt.saveBox(title = 'Save links file', fileTypes=[('Text files','*.txt')])
        with open(text_recover_path, 'a') as unfortunate_file:
            for i in range(retry_songs_number):
                unfortunate_file.write(retry_songs[i][0] + '\n' + retry_songs[i][1][0] + '\n')



syt = gui()
syt.setIcon("icon.gif")
syt.setResizable(canResize=False)
syt.setTitle('Spotifyt - by Luastan')
syt.setGuiPadding(0,0)
syt.setFont(15, font="Oswald")
syt.setBg('black')
syt.addImage("title", "title_low.gif",0,0,2)
syt.addMeter("progress",1,0,2)
syt.hideMeter("progress")
syt.setMeterBg("progress","black")
syt.setMeterPadding("progress", 0, 0)
syt.setMeterFill("progress", "purple")
syt.setMeterFg("progress", "white")
syt.addButton("Download !", hit_descarga, 1, 0)
syt.setButtonBg("Download !", 'black')
syt.setButtonSticky("Download !","both")
syt.setButtonFg("Download !", "white")
#syt.infoBox('Guia de uso', 'Open Spotify and get the playlist link in the sharing options')
is_updated()
syt.go()
#pan



if __name__ ==" __main__":
    print('Gui should be showing =)')
