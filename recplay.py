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
    top15Artists = getTop15Artists(sp)
    artistSeed = getTop2ArtistIDs(top15Artists)
    genreSeed = getTop3Genres(top15Artists)

    return sp.recommendations(seed_artists=artistSeed, seed_genres=genreSeed, limit=num, country='US')

def getSongs(sp):
    final = []
    rec = getRecommendations(sp, 5)["tracks"]
    for song in rec:
        final.append(song["name"])
    
    return final

def getURI(sp):
    final = []
    URI = getRecommendations(sp, 5)["tracks"]
    for song in URI:
        final.append(song["uri"])

    return final    


def getUserID(sp):
    userID = sp.current_user()["id"]
    return userID

def deleteTrack(sp, recommendationPlaylistID, uri):
    sp.playlist_remove_all_occurrences_of_items(recommendationPlaylistID, uri)
    return "sucess!"

def playlistLength(sp, recommendationPlaylistID):
    items = sp.playlist(playlist_id = recommendationPlaylistID)['tracks']['items']
    return str(len(items))


#making the playlist!!!

def makePlaylist(sp):
    getID = getUserID(sp)
    playlist = sp.user_playlist_create(user=getID, name="Recommendations", public=False, collaborative=False, description="A new recommendation playlisyt for you!")
    return playlist

def getRecPlaylistID(sp):
    playlistID1 = sp.current_user_playlists(limit=1, offset=0)
    playlistID2 = playlistID1["items"][0]['id']
    #filledPlaylist = sp.playlist_add_items(playlist_id=playlistID, items=getSongs(sp), position=None)
    return playlistID2 #filledPlaylist


def fillRecPlaylist(sp):
    playlistID = getRecPlaylistID(sp)
    songURIList = getURI(sp)
    filledPlaylist = sp.playlist_add_items(playlist_id=playlistID, items=songURIList, position=None)
    return filledPlaylist


