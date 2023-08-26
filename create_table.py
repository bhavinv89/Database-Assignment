# create_tables.py
from app import app, db  # Import the app instance

# Import your models if necessary
from models import Playlist, Song, PlaylistSong

# Create the database tables using the db.create_all() function
with app.app_context():
    db.create_all()
