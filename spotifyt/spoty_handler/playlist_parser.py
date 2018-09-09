'''Module used by Spotifyt to extract info about spotify playlists.
Requires the authentication module
# TODO: GEt playlist id and Username with regular expressions
'''

import spotifyt.spoty_handler.authentication
import re


SCL = spotifyt.spoty_handler.authentication.load_auth()

RE_USER_URL = re.compile(r'user\/(.*)\/playlist')
RE_ID_URL = re.compile(r'playlist\/(.*)\?')

RE_USER_URI = re.compile(r"user:(.*):playlist")
RE_ID_URI = re.compile(r":playlist:(.*)")


class playlist(object):
    """PLaylist class"""
    def __init__(self, user, id, tracks):
        if id is None:
            raise RuntimeError('Invalid playlist id.')
        if user is None:
            raise RuntimeError('Invalid playlist user.')
        super(playlist, self).__init__()
        self.id = id
        self.user = user
        self.tracks = tracks

    def __str__(self):
        text = '[i] Playlist id: {}' \
            '\n[i] Creator: {}' \
            '\n[i] Track count: {}'
        return text.format(
            self.id,
            self.user,
            len(self.tracks)
            )

    def track_count():
        def fget(self):
            return len(self.tracks)

        return locals()
    track_count = property(**track_count())


class song(object):
    """Song class to select only the necesary metadata:
        - name = song name
        - artists = All the artists in a list
        - album_name = Just the album name
        - album_img = Album image URL from Spotify
        - query = youtube query for the song"""
    def __init__(self, name, artists, album_name, album_img):
        super(song, self).__init__()
        self.name = name
        self.artists = artists
        self.album_name = album_name
        self.album_img = album_img

    def __str__(self):
        text = 'Name: {}\n' \
            'Artists: {}\n' \
            'Album: {}\n' \
            'Album img: {}'
        return text.format(
            self.name,
            self.artists,
            self.album_name,
            self.album_img
        )

    def query():
        def fget(self):
            return '{} {}'.format(
                self.name,
                self.artists[0]  # The first artist is usually the main one
            )

        return locals()
    query = property(**query())


def parse_link(link):
    if 'open.spotify.com/user/' in link:
        user = RE_USER_URL.search(link).group(1)  # Group 1 => (.*)
        id = RE_ID_URL.search(link).group(1)
        return id, user
    elif 'spotify:user:' in link:
        user = RE_USER_URI.search(link).group(1)  # Group 1 => (.*)
        id = RE_ID_URI.search(link).group(1)
        return id, user
    else:
        raise RuntimeError('Invalid playlist URL/URI.')


def get_tracks(auth, user, playlist_id):
    income = auth.user_playlist_tracks(user, playlist_id)
    tracks = income['items']
    while income['next']:  # Because the API returns songs in groups of 100
        income = auth.next(income)
        tracks.extend(income['items'])
    return tracks


def retrieve_playlist(link):
    '''Given a playlist link (URL or URI) returns a playlist object'''
    id, user = parse_link(link)

    identifications = (              # Arguments for the get_tracks function
        spotifyt.spoty_handler.authentication.load_auth(),  # Auth object
        user,                        # PLaylist user (creator)
        id                           # Playlist id
    )

    song_array = []  # Songs to be atributed to a playlist object.
    for track in get_tracks(*identifications):  # Creates song obects
        try:                                    # equivalent to the traks.
            img_url = track['track']['album']['images'][0]['url']  # 1st ++Res
        except Exception as error:
            if 'index' in str(error):  # Happens when the song has no album pic
                img_url = 'http://i.imgur.com/pb1sEG6.gif'  # SYT logo

            else:  # In case some weird exception happen
                raise error

        song_array.append(song(
            name=track['track']['name'],
            artists=[artist['name'] for artist in track['track']['artists']],
            album_name=track['track']['album']['name'],
            album_img=img_url
        ))

    return playlist(
        id=id,
        user=user,
        tracks=song_array
    )
