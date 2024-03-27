import json
from requests import post, get
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import playlist



def getTopTrackURIs(sp, artistID, country="US", num=10):
    topTracks = sp.artist_top_tracks(artist_id=artistID, country=country)['tracks']
    trackURIs = []
    for track in topTracks:
        trackURIs.append(track['uri'])
    if (num != 10):
        while (len(trackURIs) > num):
            trackURIs.pop()

    return trackURIs 

def topArtistTopTrackURIs(sp):
    """
    Gathers the top tracks from the user's top 15 artists and returns a list of all the song uris
    return: the top 15 artists' top songs
    """
    top15Artists = sp.current_user_top_artists(limit=15)['items']
    artistIDs = playlist.getArtistIDs(top15Artists)  #move this function to this file

    tracks = [] #holds a list of dictionaries of tracks
    for artistID in artistIDs:
        tracks.append(getTopTrackURIs(sp, artistID))
    final = []
    for uris in tracks: #trackURIs:
        for uri in uris:
            final.append(uri)

    return final 

def recommendedArtistTopTrackURIs(sp, recPlayistID):
    """
    Gathers the top tracks from the artists in the generated recommendation playlist
    return: recommended artist top track uris
    """
    items = sp.playlist_items(playlist_id=recPlayistID)['items']
    artists = []
    for item in items:
        artists.append(item['track']['artists'])
    artistIDs =[]
    for artist in artists:
        for info in artist:
            artistIDs.append(info['id'])

    topTracks = []
    for ids in artistIDs:
        topTracks.append(getTopTrackURIs(sp, ids, num=5))
    
    final = []
    for uris in topTracks:
        for uri in uris:
            final.append(uri)

    return final 


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


def filterHelper(sp, recPlaylistId, playlistTrackURIs, recentTrackURIs, artistTrackURIs, recommendedArtistTrackURIs):
    """
    Will filter out songs from the generated recommendation playlist. It removes songs that are in the user's
    10 most recent playlists and top tracks from their top 15 artists
    param recommendationPlaylist: the newly made recommendation playlist generated through recplay
    return: modifies the recommendation playlist so it contains never heard before new songs
    """
    recTrackURIs = getPlaylistTrackURIs(sp, recPlaylistId)

    for uri in recTrackURIs:
        if (uri in playlistTrackURIs) or (uri in recentTrackURIs) or (uri in artistTrackURIs) or (uri in recommendedArtistTrackURIs):
            playlist.deleteTrack(sp, recPlaylistId, uri)
    
    if (playlist.playlistLength(sp, recPlaylistId) < 10):
        difference = 10 - playlist.playlistLength(sp, recPlaylistId)
        newTracks = playlist.getRecommendations(sp, difference)
        sp.playlist_add_items(recPlaylistId, newTracks)
        filterHelper(sp, recPlaylistId, playlistTrackURIs, recentTrackURIs, artistTrackURIs, recommendedArtistTrackURIs)
    
def filter(sp):
    """
    Will filter out songs from the generated recommendation playlist. It removes songs that are in the user's
    10 most recent playlists and top tracks from their top 15 artists
    param recommendationPlaylist: the newly made recommendation playlist generated through recplay
    return: modifies the recommendation playlist so it contains never heard before new songs
    """
    recPlaylistId = playlist.getRecPlaylistID(sp)

    playlistTrackURIs = userPlaylistsTrackURIs(sp)
    recentTrackURIs = recentlyPlayedTrackURIs(sp)
    artistTrackURIs = topArtistTopTrackURIs(sp)
    recommendedArtistTrackURIs = recommendedArtistTopTrackURIs (sp, recPlaylistId)

    filterHelper(sp, recPlaylistId, playlistTrackURIs, recentTrackURIs, artistTrackURIs, recommendedArtistTrackURIs)

    artistNames = playlist.getArtistNames(sp, recPlaylistId)
    songNames = playlist.getSongNames(sp, recPlaylistId)

    dict = {key: value for key, value in zip(songNames, artistNames)}
    return dict


