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


class Songs:
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
        """ Grabs the top ten tracks from the given artist
        """
        top = self.sp.artist_top_tracks(self.df.loc[artist_index, 'ID'])
        top = top['tracks']
        for pos, track in enumerate(top):
            column = f'Song_{pos}'
            self.add_id(artist_index, track['id'], column)

    def add_id(self, index, spotify_id, column_name):
        """ Adds the playlist id to the corresponding row of the artist """
        self.df.loc[index, column_name] = spotify_id

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
        if index or int(index) == 0:
            pass
        else:
            return False
        if (playlist_name == playlist_check) and (creator_name == 'spotify'):
            return index
        else:
            # Playlist not found, returning artist's index.
            index = [index, 1]
            return index

    def this_is_search(self, artist_name):
        """ Searches for each artist's respective 'This is ...' playlist. """
        # Builds a query using Spotify guidelines.
        artist_query = artist_name.strip().replace(' ', '+')
        playlist = f'This+is+{artist_query}'
        search = self.sp.search(q=playlist, type='playlist', limit=1)
        search = search['playlists']['items'][0]
        playlist_name = search['name']
        creator_name = search['owner']['display_name']
        this_is_index = self.check_playlist(artist_name, playlist_name, creator_name)
        # If a playlist is found, it will add the playlist ID to the Dataframe.'
        if type(this_is_index) is int:
            self.add_id(this_is_index, search['id'], 'Playlist')
        elif type(this_is_index) is list:
            this_is_index = this_is_index[0]
            self.top_ten(this_is_index)
        else:
            # No artist in dataframe, handle it.
            pass

    def start_init_search(self):
        # Starts search for every artist.
        for name in self.df['Name']:
            self.this_is_search(name)
        return self.df


# search['playlists']['items'][0]['id']
# search['playlists']['items'][0]['name']
