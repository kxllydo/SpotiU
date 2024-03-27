import json
from requests import post, get
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import recplay


def getTrackURI(track):
    """
    Extracts the track uris
    return: the 
    """
    topTrackURIs = [trk['uri'] for trk in track]
    return topTrackURIs

def artistTopTrackURIs(sp):
    """
    Gathers the top tracks from the user's top 15 artists and returns a list of all the song uris
    return: the top 15 artists' top songs
    """
    top15Artists = recplay.getTop15Artists(sp)
    artistIDs = recplay.getArtistIDs(top15Artists)

    tracks = [] #holds a list of dictionaries of tracks
    for artistID in artistIDs:
        tracks.append(sp.artist_top_tracks(artist_id=artistID, country='US'))
    trackURIs = []
    for track in tracks: #goes into each dictionary
        tr = track['tracks']
        trackURIs.append(getTrackURI(tr)) #adds list of ids into a list
    final = []
    for uris in trackURIs:
        for uri in uris:
            final.append(uri)

    return final #returns a list of the top artists top tracks

def recentlyPlayedTrackURIs(sp):
    """
    Gets the 50 songs the user recently played
    return: 50 songs the user recently played
    """
    items = sp.current_user_recently_played()['items'] #list of all the tracks
    recentlyPlayTrackURIs = []
    for item in items:
        recentlyPlayTrackURIs.append(item['track']['uri'])
    return recentlyPlayTrackURIs

def getPlaylistTrackURIs(sp, playlistID):
    """
    Given a playlist, extract all the tracks from the playlist and return them
    pararm playlistID: the playlist id that we use to extract all the track ids from
    return: list of track ids from one single playlist
    """
    items = sp.playlist_items(playlist_id=playlistID)['items']
    tracks =[item["track"] for item in items] # a list of all the tracks from 10 playlists

    trackURIs = []
    for track in tracks: 
        trackURIs.append(track["uri"])
    return trackURIs


def userPlaylistsTrackURIs(sp):
    """
    Get all the track ids in the user's 10 recent playlists
    return: all the track ids from the user's 10 most recent playlists
    """
    playlists = sp.current_user_playlists(limit=10, offset=0)['items']  #gets the user's 10 recent playlists

    #go into items, then iterate through the list of dictionary. then go into each dictinary and get the id.
    trackURIs = []
    for playlist in playlists:
        trackURIs.append(getPlaylistTrackURIs(sp, playlist['id']))
    final = []
    for uri in trackURIs:
        for playlistID in uri:
            final.append(playlistID)
        
    return final 


def filterHelper(sp, recPlaylistId, playlistTrackURIs, recentTrackURIs, artistTrackURIs):
    """
    Will filter out songs from the generated recommendation playlist. It removes songs that are in the user's
    10 most recent playlists and top tracks from their top 15 artists
    param recommendationPlaylist: the newly made recommendation playlist generated through recplay
    return: modifies the recommendation playlist so it contains never heard before new songs
    """
    recTrackURIs = getPlaylistTrackURIs(sp, recPlaylistId)

    for uri in recTrackURIs:
        if (uri in playlistTrackURIs) or (uri in recentTrackURIs) or (uri in artistTrackURIs):
            recplay.deleteTrack(sp, recPlaylistId, uri)
    
    if (recplay.playlistLength(sp, recPlaylistId) < 5):
        difference = 5 - recplay.playlistLength(sp, recPlaylistId)
        newTracks = recplay.getRecommendations(sp, difference)
        sp.playlist_add_items(recPlaylistId, newTracks)
        filterHelper(sp, recPlaylistId, recTrackURIs, playlistTrackURIs, recentTrackURIs, artistTrackURIs)
    
    return sp.playlist(recPlaylistId)

def filter(sp, recommendationPlaylist):
    """
    Will filter out songs from the generated recommendation playlist. It removes songs that are in the user's
    10 most recent playlists and top tracks from their top 15 artists
    param recommendationPlaylist: the newly made recommendation playlist generated through recplay
    return: modifies the recommendation playlist so it contains never heard before new songs
    """
    recPlaylistId = recplay.getRecPlaylistID(sp)

    playlistTrackURIs = userPlaylistsTrackURIs(sp)
    recentTrackURIs = recentlyPlayedTrackURIs(sp)
    artistTrackURIs = artistTopTrackURIs(sp)

    hi = filterHelper(sp, recPlaylistId, playlistTrackURIs, recentTrackURIs, artistTrackURIs)
    return hi
