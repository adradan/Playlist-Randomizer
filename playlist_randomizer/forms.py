from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, ValidationError


class NumArtists(FlaskForm):
    num = []
    choices = []
    for i in range(1, 11):
        num.append(i)
        num.append(i)
        num = tuple(num)
        choices.append(num)
        num = []
    artist_num = SelectField(u'Number of Artists', choices=choices, validators=[InputRequired()])
    submit = SubmitField(label='Next')


class ChooseArtists(FlaskForm):
    pass
