import spotipy
import requests
import urllib
import re
import youtube_dl
import subprocess
import sys
import os

from appJar import gui
from spotipy.oauth2 import SpotifyClientCredentials
from threading import Thread

import tkinter as tk
import tkinter.simpledialog



import pprint


songs_to_dl =[]



def is_updated():
    readme_gh = requests.get('http://raw.githubusercontent.com/luastan/spotifyt/master/README.md')
    if not readme_gh.text[53:59] == '0.6.05':
        if syt.okBox('New Version', "There's a new version available. Would you like to download it?"):
            webbrowser.open_new_tab('https://github.com/luastan/spotifyt/releases')
            sys.exit(0)


def status_downloading():
    syt.hideButton("Download !")
    syt.showMeter("progress")


def status_patience():
    syt.hideMeter("progress")
    syt.showButton("Download !")

def print_status(current, total):
    percentage = 100*current/total

    syt.setMeter("progress", percentage, str(current) + "/" + str(total))

def downloader(song, path):

    nome = song['title'] + ' ' + song['artist']
    nome = nome.replace("/",'')
    nome = nome.replace("\\",'')
    nome = nome.replace('"','')
    nome = nome.replace("\\",'')
    nome = nome.replace("'",'')
    nome = nome.replace("?",'')
    nome = nome.replace("¿",'')
    nome = nome.replace("{",'')
    nome = nome.replace("}",'')
    nome = nome.replace("`",'')
    nome = nome.replace(",",'')
    nome = nome.replace("*",'')
    nome = nome.replace("^",'')


    full_path = path + nome + '.mp3'

    if os.path.isfile(full_path):
        print('Already Downloaded... Skipping')
        return

    if os.path.isfile('whatever.webm'):
        os.remove('whatever.webm')
    if os.path.isfile('album_pic'):
        os.remove('album_pic')

    link = youtube_search(nome)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'whatever.webm'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    print('Downloading album cover')
    cover = requests.get(song['album_pic'], stream = True)
    with open('album_pic', 'wb') as pict:
        for chunk in cover:
            pict.write(chunk)

    
    ffmpeg_args = ['ffmpeg.exe', '-i', 'whatever.webm','-i', 'album_pic', '-id3v2_version', '3', '-write_id3v1', '1', '-c', 'copy', '-map', '0', '-map', '1', '-metadata:s:v', 'title=Front Cover', '-metadata:s:v', 'comment=Cover (Front)', '-codec:a', 'libmp3lame',full_path] # 


    if not os.path.isfile(full_path):
        print('Converting to MP3')
        subprocess.call(ffmpeg_args)
    
    if os.path.isfile('whatever.webm'):
        os.remove('whatever.webm')
    if os.path.isfile('album_pic'):
        os.remove('album_pic')


    

def progressive_downloader(songs, path):
    status_downloading()
    print('Downloading')
    is_bbc = len(songs)
    current = 0
    for song in songs:
        print_status(current, is_bbc)
        downloader(song, path)
        current +=1

    status_patience()
    print('Done')
    syt.infoBox("Download completed !", "Download fully completed ! enjoy your music =) ")



def hit_descarga(btn):
    playlist_link =' https://open.spotify.com/user/luastan/playlist/2EjMDVU8sj9dr8Mdw9XYsv'
    try:
        root = tk.Tk()
        root.withdraw()
        playlist_link = root.clipboard_get()
    except:
        syt.infoBox('Copy the playlist link', 'Open Spotify and get the playlist link in the sharing options')
        return

    if playlist_link[:29] == 'https://open.spotify.com/user' or playlist_link[:13] == 'spotify:user:':
        path =  syt.directoryBox() + '/'
        spotify_raw_data = get_playlist_tracks(playlist_link)
        load_structure(spotify_raw_data)
    
            
        thread = Thread(target = progressive_downloader, args = (songs_to_dl, path))
        thread.start()
        
    else:
        syt.infoBox('Copy the playlist link', 'Open Spotify and get the playlist link in the sharing options')

def youtube_search(query):
    print('searching: ' + query)
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    enlasitos = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return 'https://youtu.be/' + enlasitos[0]

def get_playlist_tracks(playlist_link):
    #Spotify api auth
    client_credentials_manager = SpotifyClientCredentials("", "")
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    username = playlist_link.split('/')[4]
    playlist_id = playlist_link[-22:]
    print(username)
    print(playlist_id)
    
    try:
        results = sp.user_playlist_tracks(username, playlist_id)
    except:
        syt.infoBox('Copy the playlist link', 'Open Spotify and get the playlist link in the sharing options')
        return
        #Retrieve data from playlist
    tracks = results['items']
    #THis loop is required to bypass 100 track per list limit
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks







def load_structure(raw_data):
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(raw_data[0]); exit(0)
    #
    print('Stracting from Spotify')
    for raw_song_data in raw_data:
        song_details = {}
        song_details['title'] = raw_song_data['track']['name']

        artists = ''
        for saltimbanqui in raw_song_data['track']['artists']:
            artists = artists + saltimbanqui['name'] + " " 
        song_details['artist'] = artists

        try:
            album_pic = raw_song_data['track']['album']['images'][0]['url']
            song_details['album_pic'] = album_pic
        except:
            break

        songs_to_dl.append(song_details)
"""
        youtube_query = '{0} {1}'.format(song_details['title'], song_details['artist'])
        song_details['yt_link'] = youtube_search(youtube_query)
"""
        


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