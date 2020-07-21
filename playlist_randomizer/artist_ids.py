from config import Config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import playlist_randomizer.exceptions as ex
import pprint
import pandas as pd


class ArtistId:
    def __init__(self):
        self.df = None
        self.data = {'Name': [],
                     'ID': []}
        self.num_artists = None
        self.sp = None

    def create_table(self):
        self.df = pd.DataFrame(self.data)

    def authenticate(self):
        scope = 'playlist-modify-private playlist-read-private user-library-read playlist-modify-public'
        o_auth_context = {'scope': scope,
                          'client_id': Config().CLIENT_ID,
                          'client_secret': Config().CLIENT_SECRET,
                          'redirect_uri': 'http://localhost:8080',
                          'cache_path': 'cache'}
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(**o_auth_context))

    def format_artist(self, artist):
        artist = artist.lower().strip()
        artist.replace(' ', '+')
        return artist

    def search_id(self, artist):
        artist_list = []
        try:
            result = self.sp.search(q=artist, type='artist', limit=2)
            result = result['artists']['items'][0]
            artist_name = result['name']
            artist_id = result['id']
            if artist.lower() != artist_name.lower():
                no_match = ['no match', artist_name, artist_id]
                return no_match
        except IndexError:
            raise ex.ArtistNotFound(artist)
        artist_list.append(artist_name)
        artist_list.append(artist_id)
        return artist_list

    def artist_data(self, num_artists):
        self.authenticate()
        for num in range(1, num_artists + 1):
            while True:
                artist = input(f'Artist #{num}: ')
                try:
                    formatted = self.format_artist(artist)
                    search_result = self.search_id(formatted)
                    if search_result[0] == 'no match':
                        raise ex.NoDirectMatch(search_result[1])
                    self.data['Name'].append(search_result[0])
                    self.data['ID'].append(search_result[1])
                    break
                except ex.ArtistNotFound:
                    print(ex.ArtistNotFound(artist))
                except ex.NoDirectMatch:
                    print(f'{ex.NoDirectMatch(search_result[1])} Y/N')
                    confirm = input()
                    if confirm.lower().startswith('y'):
                        self.data['Name'].append(search_result[1])
                        self.data['ID'].append(search_result[2])
                        break
        self.create_table()

    def number_of_artists(self):
        while True:
            self.num_artists = input('Number of artists to include (1-10): ')
            try:
                self.num_artists = int(self.num_artists)
                if (self.num_artists < 1) or (self.num_artists > 10):
                    raise ex.OutOfRange(self.num_artists)
                else:
                    break
            except ValueError:
                print('Only enter numbers.')
            except ex.OutOfRange:
                print(ex.OutOfRange(self.num_artists))
        self.artist_data(self.num_artists)

    def start(self):
        self.number_of_artists()
        return self.df
