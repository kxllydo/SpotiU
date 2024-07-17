import spotipy
import os
import time
from spotipy.oauth2 import SpotifyOAuth
import playlist
import filter
from flask import Flask, request, url_for, session, redirect, render_template, jsonify, request
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'yaaaaassss!!!!12345'
TOKEN_INFO = 'token_info'

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    print('error?')
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('run', external = True))

@app.route('/run')
def run():
    try:
        token_info = get_token()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        createRecommendationPlaylist = playlist.makePlaylist(sp)
        filledPlaylist = playlist.makeRecommendationPlaylist(sp)
        filter.filter(sp)
        return redirect(url_for('home', external = True))
    except:
        print("User not logged in")
        return redirect('/')

@app.route('/home')
def home():  
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
<<<<<<< HEAD
    createRecommendationPlaylist = playlist.makePlaylist(sp)
    return playlist.makeRecommendationPlaylist(sp)
    # filter.filter(sp)
    # id = playlist.getRecPlaylistID(sp)
    # return render_template('home.html') #, id
=======
    id = playlist.getRecPlaylistID(sp)
    return render_template('home.html', id=id), id
>>>>>>> a9bdc9427d36d2324f3f49f2f707319ba6cfb5d0

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', external = False))

    now = int(time.time()) 

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read user-top-read playlist-modify-public playlist-modify-private user-read-private user-read-email playlist-read-private user-read-recently-played'
    )
    return sp_oauth


if __name__ == "__main__":
    app.run(debug=True)
