import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import recplay
import playfilter
from flask import Flask, request, url_for, session, redirect

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
   # recommendations = recplay.getSongs(sp) < this returns ONLY the song names from the recommended
    recommendations = recplay.getSongs(sp) # < this returns the entire dictionary info about the recommended songs
   # createRecommendationPlaylist = recplay.makePlaylist(sp)
    hi = recplay.getRecommendations(sp, 5)
    #filledPlaylist = recplay.fillRecPlaylist(sp)
    #bruh = recplay.getTop15Artists(sp)
    #id = recplay.getTop2ArtistIDs(bruh)
    playlistid = playfilter.artistTopTrackIDs(sp)
    #userplay = playfilter.userPlaylistsTrackIds(sp)
    track = playfilter.userPlaylistsTrackIds(sp)
    return track
    #id = recplay.getRecPlaylistID(filledPlaylist) <test for the id
    #ID = recplay.getUserProfile(sp)
    #return (createRecommendationPlaylist, filledPlaylist)

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
        client_id = "bbf6ac9a6686421cab10717891f179cf",
        client_secret = "e7ee05789cbd497cb1f571647c411453",
        redirect_uri = url_for('redirect_page', _external= True),
        #SCOPE COULD BE ANYTHING WE ARE ADDING!!!!
        scope = 'user-library-read user-top-read playlist-modify-public playlist-modify-private user-read-private user-read-email playlist-read-private user-read-recently-played'
        )

app.run(debug = True)