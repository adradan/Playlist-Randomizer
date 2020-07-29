from config import Config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import playlist_randomizer.exceptions as ex
import pprint
import pandas as pd
from playlist_randomizer.artist_ids import ArtistId
import pprint
import json
import time


class Playlist:
    """
    Searches for a 'This is ...' playlist for each given artist that is created by Spotify.
    Adds Playlist ID to the Pandas DataFrame.
    If none is found, finds the artists top ten songs instead.
    """
    def __init__(self):
        self.artist_id = ArtistId()
        self.df = self.artist_id.start()
        self.sp = self.artist_id.sp
        self.pp = pprint.PrettyPrinter(indent=1)

    def top_ten(self, artist_index):
        top = self.sp.artist_top_tracks(self.df.loc[artist_index, 'ID'])
        with open('tesfile', 'w+') as f:
            f.write(json.dumps(top))
        # TODO: Choose randomly from top songs at start? Or store all songs then choose randomly?
        # TODO: Pros to first: Don't have to store 10 song IDs and only have to store a couple.
        # TODO: Cons: Can't use a separate function, maybe.
        # TODO: Might just add song ids to existing DataFrame

    def add_id(self, index, playlist_id):
        """ Adds the playlist id to the corresponding row of the artist """
        self.df.loc[index, 'Playlist'] = playlist_id

    def grab_index(self, artist_name):
        """ Grabs row index of the artist """
        for index in self.df.index:
            if self.df.loc[index, 'Name'] == artist_name:
                return index
        # If there is no index with the matching artist, big problem.
        return False

    def check_playlist(self, artist_name, playlist_name, creator_name):
        """ Checks if the found playlist is an official 'This is ...' playlist.
            Compares playlist author names and playlist name. """
        artist_name = artist_name.lower().strip()
        playlist_name = playlist_name.lower().strip()
        creator_name = creator_name.lower().strip()
        playlist_check = f'this is {artist_name}'
        # If the query is both the playlist and made by Spotify,
        # continues with finding the correct index of the artist in the DF
        index = self.grab_index(artist_name.title())
        if (playlist_name == playlist_check) and (creator_name == 'spotify'):
            if index:
                return [index]
            elif int(index) == 0:
                return [index]
            else:
                return False
        else:
            index = [index, 1]
            return index

    def this_is_search(self, artist_name):
        """ Searches for each artist's respective 'This is ...' playlist. """
        # Builds a query using Spotify guidelines.
        artist_name = artist_name.strip().replace(' ', '+')
        playlist = f'This+is+{artist_name}'
        search = self.sp.search(q=playlist, type='playlist', limit=1)
        search = search['playlists']['items'][0]
        playlist_name = search['name']
        creator_name = search['owner']['display_name']
        this_is_index = self.check_playlist(artist_name, playlist_name, creator_name)
        # If a playlist is found, it will add the playlist ID to the Dataframe.'
        if len(this_is_index) == 1:
            # self.add_id(this_is_index, search['id'])
            self.top_ten(this_is_index)
        elif len(this_is_index) == 2:
            # If the playlist is not found. It will search for the top ten tracks.
            self.top_ten(this_is_index)
        else:
            # TODO: No such artist is in DataFrame, figure out how to handle.
            pass

    def start_init_search(self):
        # Starts search for every artist.
        for name in self.df['Name']:
            self.this_is_search(name)
        print(self.df)


Playlist().start_init_search()

# search['playlists']['items'][0]['id']
# search['playlists']['items'][0]['name']
