import os


class Config:
    def __init__(self):
        self.CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
        self.REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')