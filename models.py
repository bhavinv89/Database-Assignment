from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

class PlaylistSongs(db.Model):
    __tablename__ = 'playlist_songs'
    
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    song = db.relationship('Song', backref='playlist_songs')
    playlist = db.relationship('Playlist', backref='playlist_songs')

# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
