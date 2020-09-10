from playlist_randomizer.songs import Songs
import json


class Playlist:
    def __init__(self):
        self.playlist = None
        self.song = Songs()
        self.df = self.song.start_init_search()
        self.sp = self.song.sp
        self.user = self.sp.current_user()
        self.songs = []
        # self.user_name = self.user['display_name']
        # self.user_id = self.user['id']
        print(self.df)
        self.create_playlist()

    def create_playlist(self):
        user_name = self.user['display_name']
        user_id = self.user['id']
        playlist_name = f'This is {user_name}'
        description = f'Compilation of {user_name}\'s favorite artists.'
        context = {'user': user_id,
                   'name': playlist_name,
                   'public': True,
                   'description': description}
        self.grab_ids()
        self.playlist = self.sp.user_playlist_create(**context)
        self.add_songs(user_id)

    def grab_ids(self):
        for i in range(0, 10):
            song_num = f'Song_{i}'
            song_ids = self.df[song_num].values
            for s_id in song_ids:
                self.songs.append(s_id)
        print(self.songs)

    def add_songs(self, user_id):
        pl_id = self.playlist['id']
        self.sp.user_playlist_add_tracks(user_id, pl_id, self.songs)



Playlist()
