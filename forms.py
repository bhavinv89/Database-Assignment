from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = StringField('Description', validators=[Length(max=500)])
    submit = SubmitField('Create Playlist')

class SongForm(FlaskForm):
    """Form for adding songs."""
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    artist = StringField('Artist', validators=[DataRequired(), Length(min=1, max=100)])
    duration = IntegerField('Duration (in seconds)', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Create Song')



# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
    playlist = SelectField('Playlist', coerce=int)
