import json
from requests import post, get
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

# returns a list of dictionaries, each dictionary being info about the artist
def getTop15Artists(sp):
    return sp.current_user_top_artists(limit=15)['items']

def getArtistIDs(artists):
    artistID = [artist["id"] for artist in artists]
    return artistID

# returns a list of the top 2 artists ids 
def getTop2ArtistIDs(top15Artists):
    artistIDs = getArtistIDs(top15Artists)
    return [artistIDs[0], artistIDs[1]]

# gets top 3 genres from the list of 15 artist
def getTop3Genres(top15Artists):
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
    param num: The number of songs you want the request to randomly generate
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
    items = sp.playlist_items(playlistID)['items']
    songNames = []
    for item in items:
        songNames.append(item['track']['name'])

    return songNames

def getArtistNames(sp, playlistID):
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
    userID = sp.current_user()["id"]
    return userID

def deleteTrack(sp, recommendationPlaylistID, uri):
    sp.playlist_remove_all_occurrences_of_items(recommendationPlaylistID, [uri])

def playlistLength(sp, recommendationPlaylistID):
    items = sp.playlist(playlist_id = recommendationPlaylistID)['tracks']['items']
    return len(items)

def makePlaylist(sp):
    getID = getUserID(sp)
    playlist = sp.user_playlist_create(user=getID, name="Recommendations", public=False, collaborative=False, description="A new recommendation playlisyt for you!")
    return playlist

def getRecPlaylistID(sp):
    playlists = sp.current_user_playlists(limit=1, offset=0)
    playlistID = playlists["items"][0]['id']
    return playlistID

def makeRecommendationPlaylist(sp):
    playlistID = getRecPlaylistID(sp)
    songURIList = getRecommendations(sp, 10)
    filledPlaylist = sp.playlist_add_items(playlist_id=playlistID, items=songURIList, position=None)
    return filledPlaylist


