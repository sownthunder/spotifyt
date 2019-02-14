#!/usr/bin/env python3

from os import system
from sys import platform
from setuptools import setup

def addToBin():
  f = open('/bin/spotifyt', 'w')
  print('python3 -m spotifyt -h', file=f)
  f.close()
  system("chmod +x /bin/spotifyt")


setup(name='spotifyt',
      version='0.8',
      description='Download songs from your Spotify playlists',
      author='Luastan',
      url='https://github.com/luastan/spotifyt',
      packages=[
        'spotifyt',
        'spotifyt.media_handler',
        'spotifyt.spoty_handler'],
      install_requires=[
        'requests==2.19.1',
        'youtube-dl==2018.9.8',
        'spotipy==2.4.4',
        ],
      )

if platform == 'linux' or platform == 'linux32':
  addToBin()