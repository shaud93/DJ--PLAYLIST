"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Playlist Database #
class Playlist(db.Model):
    """Playlist."""

    __tablename__ = "playlist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    desc = db.Column(db.String(40))
    pls = db.relationship("PlaylistSong", backref = "p")



# Song & Playlist Database #
class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__="playlist_song"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id"))
    song_id = db.Column(db.Integer, db.ForeignKey("song.id"))




# Song Database #
class Song(db.Model):
    """Song."""

    __tablename__= "song"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    artist = db.Column(db.String(25), nullable=False)
    pls = db.relationship("PlaylistSong", backref = "s")






# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
