import spotipy
import json
import time
from spotipy.oauth2 import SpotifyOAuth
import playlist
import filter
from flask import Flask, request, url_for, session, redirect, render_template

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'yaaaaassss!!!!12345'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('home', external = True))

@app.route('/home')
def home():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    bruh = filter.recommendedArtistTopTrackURIs(sp, '1pSq0tMtVlsHWJIR62Hokc')
    createRecommendationPlaylist = playlist.makePlaylist(sp)
    filledPlaylist = playlist.makeRecommendationPlaylist(sp)
    hi = filter.filter(sp)

    return render_template('home.html') 

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
    return SpotifyOAuth(
        client_id = "c584a76f0e49433ab86e6b25fcc3aa2b",
        client_secret = "d40de1a1f2a14c5d845543c6680ed642",
        redirect_uri = url_for('redirect_page', _external= True),
        #SCOPE COULD BE ANYTHING WE ARE ADDING!!!!
        scope = 'user-library-read user-top-read playlist-modify-public playlist-modify-private user-read-private user-read-email playlist-read-private user-read-recently-played'
        )

app.run(debug = True)