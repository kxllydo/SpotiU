import json
from requests import post, get
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import recplay


def getTrackID(track):
    tr = track['tracks']
    topTrackIDs = [trk['id'] for trk in tr]
    return topTrackIDs

def getArtistTopTracksID(sp):
    top15Artists = recplay.getTop15Artists(sp)
    artistIDs = recplay.getArtistIDs(top15Artists)

    tracks = [] #holds a list of dictionaries of tracks
    for artist in artistIDs:
        tracks.append(sp.artist_top_tracks(artist_id=artist, country='US'))
    trackIDs = []
    for track in tracks: #goes into each dictionary
        trackIDs.append(getTrackID(track)) #adds list of ids into a list
    final = []
    for ids in trackIDs:
        for id in ids:
            final.append(id)

    return final

#goal is to get track ids

def recentlyPlayedTrackIDs:
    

    
    