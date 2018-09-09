"""Main Spotifyt module. Intended for argument parsing"""

import argparse
import sys
import tempfile
import os

import spotifyt.spoty_handler.playlist_parser
import spotifyt.spoty_handler.authentication
import spotifyt.media_handler.downloader
import spotifyt.banner

SYT_TMP_DIR = tempfile.gettempdir() + '/spotifyt/'
VERSION = '0.8'
CODENAME = 'Banana'
RUN_INFO = """  Author: @luastan\n""" \
           """  Spotifyt version: {}    -    Codename: {}\n""" \
           """  Playlists queued: {}      -    Download directory: {}\n"""
DESCRIPTION = """Song download automation via CLI by @luastan"""


def print_banner():
    '''Prints Spotifyt in ASCII art'''
    print(spotifyt.banner.out())


def main(args):
    download_dir = args.d + '/' if args.d else './'
    print(RUN_INFO.format(
        VERSION,
        CODENAME,
        len(args.playlist),
        download_dir
    ))

    if not os.path.exists(SYT_TMP_DIR):
        print('[+] Creating temoporary directory at {}...'.format(SYT_TMP_DIR))
        os.makedirs(SYT_TMP_DIR)

    if not os.path.exists(download_dir):
        print('[+] Creating download directory at {}...'.format(download_dir))
        os.makedirs(download_dir)

    for req in args.playlist:
        print('\n[+] Current playlist info:')
        print('[*] Input link: {}'.format(req))
        sys.stdout.flush()
        list = spotifyt.spoty_handler.playlist_parser.retrieve_playlist(req)
        print(list)
        sys.stdout.flush()
        for song in list.tracks:
            search = spotifyt.media_handler.downloader.yt_search(song.query)
            sys.stdout.flush()
            spotifyt.media_handler.downloader.yt_downloader(
                search,
                download_dir,
                song
            )

    print("\n[!] Done :)")


if __name__ == '__main__':
    print_banner()
    parser = argparse.ArgumentParser(
        prog='spotifyt',
        description=DESCRIPTION
    )

    parser.add_argument(
        'playlist',
        metavar='PLAYLIST',
        type=str,
        nargs='*',
        help='Spotify\'s playlist URL/URI to download'
    )

    parser.add_argument(
        '-d',
        metavar='DIRECTORY',
        type=str,
        nargs='?',
        help='Download Directory'
    )

    parser.add_argument(
        '-k',
        action='store_true',
        help='Delete saved API keys'
    )

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(VERSION)
                        )

    args = parser.parse_args()

    if args.k:
        spotifyt.spoty_handler.authentication.remove_api_keys()
        exit(0)

    if len(args.playlist) == 0:
        "[!] No playlists provided. Exiting..."
        exit(1)

    main(args)
