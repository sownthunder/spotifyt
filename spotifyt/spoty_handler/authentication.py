'''Authentication module for Spotifyt. Mainly to deal with the API auth
API KEYS stored at API_KEYS_LOCATION (Check global variables)
'''

import spotipy
import json
import os
from spotipy.oauth2 import SpotifyClientCredentials
import sys


SPOTIFYT_DIR = os.environ['HOME'] + "/.spotifyt/"  # Default settings location
API_KEYS_LOCATION = SPOTIFYT_DIR + "api_auth.json"  # Default keyfile name


def auth(client_id, client_secret):
    '''Returns Spotipy auth object necessary to use the spotify API'''
    client_cred_mgr = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_cred_mgr)
    return sp


def api_key_saver(client_id, client_secret):
    '''Writes given API keys to API_KEYS_LOCATION
    If the directory doesn't exist it gets created'''

    if not os.path.exists(SPOTIFYT_DIR):
        print('[+] Creating the file...')
        os.makedirs(SPOTIFYT_DIR)

    api_keys = {  # json format
        "client_id": client_id,
        "client_secret": client_secret
    }

    with open(API_KEYS_LOCATION, "w+") as api_keys_json:  # Saves the json
        api_keys_json.write(json.dumps(api_keys))
        api_keys_json.close()


def load_auth():
    '''Looks for the API keys file
    If the file doesn't exsist it's created and the user promted to input
    his credentials.
    If the file does exist, an spotipy client auth object is returned'''
    try:  # Checks for the file existance mainly
        with open(API_KEYS_LOCATION, "r") as api_creds_json:
            keys = json.load(api_creds_json)
            return auth(**keys)

    except Exception as load_err:
        if 'No such file or directory' in str(load_err):
            print('[!] No API keys file found')
            print('[i] Get your keys at {}'.format(
                'https://developer.spotify.com'
            ))
            sys.stdout.flush()
            api_key_saver(
                input('[?] Type client id: '),
                input('[?] Type client secret: '))
        else:  # Just in case the exception is not the one expected
            raise load_err


def remove_api_keys():
    '''Removes the Spotifyt directory where API keys are stored'''
    os.remove(SPOTIFYT_DIR)
