from playlist_randomizer import app, sp
from playlist_randomizer import forms
from flask import render_template


@app.route('/')
def home():
    form = forms.Artists()
    return render_template('base.html', form=form)

@app.route('/choose')
def artist_choice():
    form = forms.ChooseArtists()
    