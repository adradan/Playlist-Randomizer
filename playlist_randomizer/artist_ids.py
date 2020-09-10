import playlist_randomizer.exceptions as ex
import pandas as pd
from playlist_randomizer import authenticate



def format_artist(artist):
    """ Formats given artist for use with queries """
    artist = artist.lower().strip()
    artist.replace(' ', '+')
    return artist

class ArtistId:
    """
    Asks for a number of artists and searches for them within Spotify
    Adds each Artist's Spotify ID and Name into a DataFrame and will throw errors if no matches are found.
    """
    def __init__(self):
        self.df = None
        self.data = {'Name': [],
                     'ID': []}
        self.num_artists = None
        self.sp = None

    def create_table(self):
        """ Creates a DataFrame """
        self.df = pd.DataFrame(self.data)

    def search_id(self, artist):
        """
        Searches for Artist
        Will return no match if not exact artist is found, otherwise, returns artist id and name
        """
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
        """ Asks for Artists, will add artist info to a list which will later be turned into a DF """
        self.sp = authenticate.auth()
        for num in range(1, num_artists + 1):
            while True:
                artist = input(f'Artist #{num}: ')
                try:
                    formatted = format_artist(artist)
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

    def number_of_artists(self):
        """ Asks for how many artists they want """
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

    def start(self):
        """ Starts process """
        self.number_of_artists()
        self.artist_data(self.num_artists)
        self.create_table()
        return self.df
