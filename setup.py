#!/usr/bin/env python3

from setuptools import setup

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
