from playlist_randomizer.songs import Songs


class Playlist:
    def __init__(self):
        self.df = Songs().start_init_search()
        print(self.df)

    def song_list(self):
        pass




Playlist()
