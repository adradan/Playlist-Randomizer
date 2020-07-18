from playlist_randomizer import app, sp
from playlist_randomizer import forms


@app.route('/')
def home():
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
    form = forms.Artists()
    return 'Hello, world!'
