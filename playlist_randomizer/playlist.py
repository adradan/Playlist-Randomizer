from playlist_randomizer.songs import Songs


class Playlist:
    def __init__(self):
        self.playlist = None
        self.song = Songs()
        self.df = self.song.start_init_search()
        self.sp = self.song.sp
        self.user = self.sp.current_user()
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
        self.playlist = self.sp.user_playlist_create(**context)


Playlist()
