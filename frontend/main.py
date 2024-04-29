from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import time
from flask import Flask, request, url_for, session, redirect, render_template, jsonify, request
from dotenv import load_dotenv
import os
import json

test = Flask(__name__)

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
test.secret_key = 'yaaaaassss!!!!12345'
test.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'

TOKEN_INFO = 'token_info'

@test.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@test.route('/redirect')
def redirect_page():
    print('error?')
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('home', external = True))

@test.route('/home')
def home():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    # createRecommendationPlaylist = playlist.makePlaylist(sp)
    # filledPlaylist = playlist.makeRecommendationPlaylist(sp)
    # hi = filter.filter(sp)
    
    return jsonify(token_info) #render_template('home.html') 

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
    test.run()

