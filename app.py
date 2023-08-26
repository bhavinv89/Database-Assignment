from flask import Flask, redirect, render_template, redirect, url_for, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from sqlalchemy.sql import func

# Import your SQLAlchemy models after initializing db
from models import db, connect_db, Playlist,Song, PlaylistSongs
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

# Initialize the SQLAlchemy database
db.init_app(app)  # This line initializes the app with the database

# This function creates the database tables. Wrap it in an application context.
with app.app_context():
    db.create_all()


# Create the Debug Toolbar extension
debug = DebugToolbarExtension(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)


@app.route('/')
def playlists():
    """Homepage: Welcome to playlists."""
    print('test')
    return render_template('base.html')



##############################################################################
# Playlist routes

@app.route("/playlists",methods=['GET', 'REQUEST'])
def show_all_playlists():
    """Return a list of playlists."""
    print('Hello world!')
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template("playlist.html", playlist=playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:"""
    form = NewSongForPlaylistForm()
    form.song.choices = [(song.id, song.title) for song in Song.query.all()]
    form.playlist.choices = [(playlist.id, playlist.name) for playlist in Playlist.query.all()]
    if form.validate_on_submit():
        for song_id in form.song.data:
            song = Song.query.get(song_id)
            for playlist_id in form.playlist.data:
                playlist = Playlist.query.get(playlist_id)
                playlist.songs.append(song)
        db.session.commit()
        return redirect(url_for('show_playlists'))
    return render_template('add_song_to_playlist.html', form=form, playlist=playlist)


##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/song/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    form = SongForm()
    if form.validate_on_submit():
        song = Song(title=form.title.data)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('show_songs'), form=form)
    return render_template('song.html')


@app.route('/songs/add/<int:playlist_id>', methods=["GET", "POST"])
def add_song(playlist_id):
    """Handle add-song form: """
    form = NewSongForPlaylistForm()
    form.song.choices = [(song.id, song.title) for song in Song.query.all()]
    form.playlist.choices = [(playlist.id, playlist.name) for playlist in Playlist.query.all()]
    if form.validate_on_submit():
        for song_id in form.song.data:
            song = Song.query.get(song_id)
            for playlist_id in form.playlist.data:
                playlist = Playlist.query.get(playlist_id)
                playlist.songs.append(song)
        db.session.commit()
        return redirect(url_for('playlist_songs', playlist_id=playlist_id))
    return render_template('add_song_to_playlist.html', form=form, playlist=playlist)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist

    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = (db.session.query(Song.id, Song.title)
                      .filter(Song.id.notin_(curr_on_playlist))
                      .all())

    if form.validate_on_submit():

          # This is one way you could do this ...
      playlist_song = PlaylistSong(song_id=form.song.data,
                                  playlist_id=playlist_id)
      db.session.add(playlist_song)

      # Here's another way you could that is slightly more ORM-ish:
      #
      # song = Song.query.get(form.song.data)
      # playlist.songs.append(song)

      # Either way, you have to commit:
      db.session.commit()

    return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)
