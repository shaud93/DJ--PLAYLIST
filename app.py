from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
import functions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "I Like Eggs"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)

    # returns all song Titles in playlist
    songs_on_playlist = functions.Get_Playlist_Songs(playlist.pls)

    return render_template("playlist.html", playlist=playlist, songs_on_playlist=songs_on_playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        name = form.name.data
        desc = form.desc.data
        send_to_db = Playlist(name=name.upper(), desc=desc)
        db.session.add(send_to_db)
        db.session.commit()
        return redirect("/playlists")
    else:
        return render_template("new_playlist.html", form=form)
    


##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    song = Song.query.get_or_404(song_id)
    song_playlist = functions.Get_Song_Playlist(song.pls)
    return render_template("song.html", song=song, song_playlist=song_playlist)



@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        name = form.name.data
        artist = form.artist.data
        send_to_db = Song(name=name.upper(), artist=artist.upper())
        db.session.add(send_to_db)
        db.session.commit()
        return redirect("/songs")
    else:
        return render_template("new_song.html", form=form)

    


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    #get all songs
    songs = Song.query.all()

    

    # returns all song Titles in playlist
    songs_on_playlist = functions.Get_Playlist_Songs(playlist.pls)

    form.song.choices = [(songs.id, songs.name) for songs in songs]

    if form.validate_on_submit():
        added_song = Song.query.get_or_404(form.song.data) 
        # Restrict form to songs not already on this playlist
        if added_song.name in songs_on_playlist:
            flash(f"{added_song.name} is already in playlist")
            return redirect(f"/playlists/{playlist_id}")
        flash(f"added {added_song.name}")
        send_to_db = PlaylistSong(playlist_id=playlist_id, song_id=added_song.id)
        db.session.add(send_to_db)
        db.session.commit()
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html", playlist=playlist,form=form)
