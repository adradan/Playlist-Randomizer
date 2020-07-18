from config import Config
from flask import Flask
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'playlist-modify-private playlist-read-private user-library-read'

OAuth_context = {'scope': scope,
                 'client_id': Config().CLIENT_ID,
                 'client_secret': Config().CLIENT_SECRET,
                 'redirect_uri': 'http://localhost:8080',
                 'cache_path': 'cache'}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(**OAuth_context))

app = Flask(__name__)
app.config.from_object(Config)

from playlist_randomizer import routes

