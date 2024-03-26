import json
from requests import post, get
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import recplay


def getTrackID(track):
    """
    Extracts the track ids
    return: the 
    """
    topTrackIDs = [trk['id'] for trk in track]
    return topTrackIDs

def artistTopTrackIDs(sp):
    """
    Gathers the top tracks from the user's top 15 artists and returns a list of all the song ids
    return: the top 15 artists' top songs
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



def recentlyPlayedTrackIDs(sp):
    """
    Gets the 50 songs the user recently played
    return: 50 songs the user recently played
    """
    items = sp.current_user_recently_played()['items'] #list of all the tracks
    recentlyPlayTrackID = []
    for item in items:
        recentlyPlayTrackID.append(item['track']['id'])
    return recentlyPlayTrackID




def getPlaylistTrackIDs(sp, playlistID):
    """
    Given a playlist, extract all the tracks from the playlist and return them
    pararm playlistID: the playlist id that we use to extract all the track ids from
    return: list of track ids from one single playlist
    """
    items = sp.playlist_items(playlist_id=playlistID)['items']
    tracks =[item["track"] for item in items] # a list of all the tracks from 10 playlists

    trackIDs = []
    for track in tracks: 
        trackIDs.append(track["id"])
    return trackIDs


def userPlaylistsTrackIds(sp):
    """
    Get all the track ids in the user's 10 recent playlists
    return: all the track ids from the user's 10 most recent playlists
    """
    playlists = sp.current_user_playlists(limit=10, offset=0)['items']  #gets the user's 10 recent playlists

    #go into items, then iterate through the list of dictionary. then go into each dictinary and get the id.
    trackIDs = []
    for playlist in playlists:
        trackIDs.append(getPlaylistTrackIDs(sp, playlist['id']))
    final = []
    for ids in trackIDs:
        for playlistID in ids:
            final.append(playlistID)
        
    return final 


# def filter(sp, recommendationPlaylist):
#     """
#     Will filter out songs from the generated recommendation playlist. It removes songs that are in the user's
#     10 most recent playlists and top tracks from their top 15 artists
#     param recommendationPlaylist: the newly made recommendation playlist generated through recplay
#     return: modifies the recommendation playlist so it contains never heard before new songs
#     """
#     recPlaylistId = recplay.getRecPlaylistID(sp)
#     recTrackIds = getPlaylistTrackIDs(sp, recPlaylistId)

#     playlistTrackIds = userPlaylistsTrackIds(sp)
#     recentTrackIds = recentlyPlayedTrackIDs(sp)
#     artistTrackIds = artistTopTrackIDs(sp)

#     for id in recTrackIds:
#         if (id in playlistTrackIds) or (id in recentTrackIds) or (id in artistTrackIds):





    



    
    