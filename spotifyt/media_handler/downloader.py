'''Intended to handle youtube downloads and the album pic from spotify'''

import requests
import youtube_dl
import urllib
import re
import subprocess
import tempfile
import os
import hashlib

YT_QUERY_BASE = 'https://www.youtube.com/results?'
YT_LINK_R = r'href=\"\/watch\?v=(.{11})'
YT_WATCH_BASE = 'https://www.youtube.com/watch?'
SYT_TMP_DIR = tempfile.gettempdir() + '/spotifyt/'


def yt_search(query):
    '''Given a query, returns the firt result link'''
    print('[*] Searching    -> {}'.format(query))
    encoded_query = urllib.parse.urlencode({"search_query": query})
    print(YT_QUERY_BASE + encoded_query)

    r = requests.get(YT_QUERY_BASE + encoded_query)
    id = re.search(YT_LINK_R, r.text).group(1)  # .group(1)=> (.{11})
    encoded_id = urllib.parse.urlencode({"v": id})
    link = YT_WATCH_BASE + encoded_id
    print('[+] Result found -> {}'.format(link))
    return link


def yt_downloader(link, directory, song):
    '''DOwnloads a given song_objet on a directory and converts it to mp3 with
    ffmpeg'''
    hashed_link = hashlib.sha1(link.encode()).hexdigest()
    tmp_webm = SYT_TMP_DIR + hashed_link + '.webm'
    tmp_pic = SYT_TMP_DIR + hashed_link + '.jpg'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tmp_webm
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    print('[*] Downloading album cover')
    cover = requests.get(song.album_img, stream=True)

    with open(tmp_pic, 'wb') as pict:
        for chunk in cover:
            pict.write(chunk)

    full_path = directory + song.name + '.mp3'
    print("[*] Converting to mp3...")
    ffmpeg_args = [  # FFMpeg argumetns
        'ffmpeg',
        '-loglevel',
        'panic',
        '-i',
        tmp_webm,
        '-i',
        tmp_pic,
        '-id3v2_version',
        '3',
        '-write_id3v1',
        '1',
        '-c',
        'copy',
        '-map',
        '0',
        '-map',
        '1',
        '-metadata:s:v',
        'title=Front Cover',
        '-metadata:s:v',
        'comment=Cover (Front)',
        '-codec:a',
        'libmp3lame',
        full_path
    ]
    subprocess.call(ffmpeg_args)
    print('[i] Finished conversion.')
    print('[-] Cleaning temporary files.')
    for tmp_file in [tmp_webm, tmp_pic]:  # Removes temporary files
        if os.path.isfile(tmp_file):
            os.remove(tmp_file)
