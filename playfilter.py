import json
from requests import post, get
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import recplay


def getTrackID(track):
    """
    Extracts the track ids
    """
    topTrackIDs = [trk['id'] for trk in track]
    return topTrackIDs

def getArtistTopTracksID(sp):
    """
    Gathers the top tracks from the user's top 15 artists and returns a list of all the song ids
    """
    top15Artists = recplay.getTop15Artists(sp)
    artistIDs = recplay.getArtistIDs(top15Artists)

    tracks = [] #holds a list of dictionaries of tracks
    for artistID in artistIDs:
        tracks.append(sp.artist_top_tracks(artist_id=artistID, country='US'))
    trackIDs = []
    for track in tracks: #goes into each dictionary
        tr = track['tracks']
        trackIDs.append(getTrackID(tr)) #adds list of ids into a list
    final = []
    for ids in trackIDs:
        for id in ids:
            final.append(id)

    return final #returns a list of the top artists top tracks


#goal is to get track ids

#def recentlyPlayedTrackIDs:

def playlistTrackIDHelper(sp, playlistID): #individually get a dictionary, go into items
    """
    Given a playlist, extract all the tracks from the playlist and return them
    pararm playlistID: the playlist id that we use to extract all the track ids from
    """
    items = sp.playlist_items(playlist_id=playlistID)['items']

    tracks =[item["track"] for item in items] # a list of all the tracks from 10 playlists

    trackIDs = []
    for track in tracks: 
        trackIDs.append(track["id"])

    return trackIDs





#for some reason it displays only 3 sometimes
def userPlaylistsTrackIds(sp):
    """
    Trying to get all the tracks in the user's 10 recent playlists
    """
    playlists = sp.current_user_playlists(limit=10, offset=0)['items']  #gets the user's 10 recent playlists

    #go into items, then iterate through the list of dictionary. then go into each dictinary and get the id.
    playlistIDs = [] #all the playlist id
    for playlist in playlists:
        playlistIDs.append(playlist['id'])


    trackIDs = []
    for playlistID in playlistIDs:
        trackIDs.append(playlistTrackIDHelper(sp, playlistID))

    final = []
    for ids in trackIDs:
        for playlistID in ids:
            final.append(playlistID)
        
    return final 





    
    