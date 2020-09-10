from config import Config
from spotipy.oauth2 import SpotifyOAuth
import spotipy


def auth():
    """ Authenticates with O Auth asking for scopes """
    scope = 'playlist-modify-private playlist-read-private user-library-read playlist-modify-public'
    o_auth_context = {'scope': scope,
                      'client_id': Config().CLIENT_ID,
                      'client_secret': Config().CLIENT_SECRET,
                      'redirect_uri': 'http://localhost:8080',
                      'cache_path': 'cache'}
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(**o_auth_context))
    return sp
