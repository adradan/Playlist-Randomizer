from config import Config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import playlist_randomizer.exceptions as ex
import pprint
import pandas as pd
from playlist_randomizer.artist_ids import ArtistId
import pprint


class Playlist:
    def __init__(self):
        self.artist_id = ArtistId()
        self.df = self.artist_id.start()
        self.sp = self.artist_id.sp
        self.pp = pprint.PrettyPrinter(indent=1)

    def top_ten(self):
        pass

    def add_id(self, index, playlist_id):
        self.df.loc[index, 'Playlist'] = playlist_id

    def grab_index(self, artist_name):
        for index in self.df.index:
            if self.df.loc[index, 'Name'] == artist_name:
                return index
        return False

    def check_playlist(self, artist_name, playlist_name):
        artist_name = artist_name.lower().strip()
        playlist_name = playlist_name.lower().strip()
        playlist_check = f'this is {artist_name}'
        if playlist_name == playlist_check:
            index = self.grab_index(artist_name.title())
            if index:
                return index
            elif int(index) == 0:
                return index
            else:
                return False

    def this_is_search(self, artist_name):
        artist_name = artist_name.strip()
        playlist = f'This is {artist_name}'
        search = self.sp.search(q=playlist, type='playlist', limit=1)
        search = search['playlists']['items'][0]
        this_is_index = self.check_playlist(artist_name, search['name'])
        if this_is_index:
            self.add_id(this_is_index, search['id'])
        elif int(this_is_index) == 0:
            self.add_id(this_is_index, search['id'])
        else:
            self.top_ten()

    def start_init_search(self):
        for name in self.df['Name']:
            self.this_is_search(name)
        print(self.df)


Playlist().start_init_search()

# search['playlists']['items'][0]['id']
# search['playlists']['items'][0]['name']
