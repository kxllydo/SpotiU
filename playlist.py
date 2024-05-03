import json
from requests import post, get
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

def getTop15Artists(sp):
    """
    Gets the top 15 artists from the user

    return: a list of the top 15 artists the user listens to
    """
    return sp.current_user_top_artists(limit=15)['items']

def getArtistIDs(artists):
    """
    Extracts the artist id given a list of artists
    
    return: a string of the top 15 artists the user listens to
    """
    artistID = [artist["id"] for artist in artists]
    return artistID

def getTop2ArtistIDs(top15Artists):
    """
    Gets the top 2 artists' ids from the user
    
    return: a list of the top 2 artists' ids the user listens to
    """
    artistIDs = getArtistIDs(top15Artists)
    return [artistIDs[0], artistIDs[1]]

def getTop3Genres(top15Artists):
    """
    Gets the top 3 artists from the user
    
    return: list of the top 3 genres the user listens to
    """
    artist_genres = [genres ["genres"] for genres in top15Artists]
    listOfGenres = []
    for genres in artist_genres:
        for genre in genres:
            listOfGenres.append(genre)  #regular list of genres 

    frequency = {}
    for item in listOfGenres:
        if item in frequency:
            frequency [item] += 1
        else:
            frequency[item] = 1

    tupleFrequency = frequency.items()
    sortedTupleFrequency = sorted(tupleFrequency, key = lambda x : x[1], reverse= True)

    finalGenres = []
    for i in range (3):
        topGenre = sortedTupleFrequency[i][0]
        finalGenres.append(topGenre)

    return finalGenres

def getRecommendations(sp, num):
    """
    Returns a list of track uris of songs that spotify generated

    @param num: The number of songs you want the request to randomly generate
    return: a list of uris of songs that spotify recommended
    """
    top15Artists = getTop15Artists(sp)
    artistSeed = getTop2ArtistIDs(top15Artists)
    genreSeed = getTop3Genres(top15Artists)
    recommendations = sp.recommendations(seed_artists=artistSeed, seed_genres=genreSeed, limit=num, country='US')['tracks']
    URIs = []
    for track in recommendations:
        URIs.append(track['uri'])

    return URIs


def getSongNames(sp, playlistID):
    """
    Gets the name of all the songs in a given playlist

    @param playlistID: The id of the playlist you want to get the song names from
    return: a list of song names
    """
    items = sp.playlist_items(playlistID)['items']
    songNames = []
    for item in items:
        songNames.append(item['track']['name'])

    return songNames

def getArtistNames(sp, playlistID):
    """
    Gets the name of all the artists of the songs in a given playlist

    @param playlistID: The id of the playlist you want to get the artists names from
    return: a list of artists names
    """
    items = sp.playlist_items(playlistID)['items']
    allArtist = []
    for item in items:
        allArtist.append(item['track']['artists'])
    
    artistNames = []
    for artists in allArtist:
        if (len(artists) > 1):
            collabArtists = []
            for artist in artists:
                collabArtists.append(artist['name'])
            artistNames.append(collabArtists)
        else:
            artistNames.append(artists[0]['name'])

    return artistNames


def getUserID(sp):
    """
    Gets the user id

    return: string of user id
    """
    userID = sp.current_user()["id"]
    return userID

def deleteTrack(sp, recommendationPlaylistID, uri):
    """
    Deletes a track or set of tracks from the recommendation playlist

    @param recommendationPlaylistID: the id of the recommendation playlist
    @param uri: a list of uris of songs you want to delete
    """
    sp.playlist_remove_all_occurrences_of_items(recommendationPlaylistID, [uri])

def playlistLength(sp, recommendationPlaylistID):
    """
    Finds the length of a playlist

    return: an integer representing the length of the playlist
    """
    items = sp.playlist(playlist_id = recommendationPlaylistID)['tracks']['items']
    return len(items)

def makePlaylist(sp):
    """
    Creates a playlist on the user's account titled "Recommendations"

    return: the new playlist created
    """
    getID = getUserID(sp)
    playlist = sp.user_playlist_create(user=getID, name="Recommendations", public=False, collaborative=False, description="A new recommendation playlist for you!")
    return playlist

def getRecPlaylistID(sp):
    """
    Gets the recommendation playlist id

    return: the recommendation playlist id
    """
    playlists = sp.current_user_playlists(limit=1, offset=0)
    playlistID = playlists["items"][0]['id']
    return playlistID

def makeRecommendationPlaylist(sp):
    """
    Generates the recommendation playlist on the user's account

    return: the new recommendation playlist
    """
    playlistID = getRecPlaylistID(sp)
    songURIList = getRecommendations(sp, 10)
    filledPlaylist = sp.playlist_add_items(playlist_id=playlistID, items=songURIList, position=None)
    return filledPlaylist


