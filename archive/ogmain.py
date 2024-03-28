import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

print(client_id, client_secret)

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {

        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_authorization_code():
    # Direct the user to Spotify Accounts service for authentication
    auth_url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri=https://accounts.spotify.com/authorize&scope=user-top-read'
    
    print(f"Please visit the following URL to authorize your application:\nhttps://accounts.spotify.com/authorize")

    # Input the authorization code obtained from the redirect URI
    authorization_code = input("Enter the authorization code from the redirect URI: ")
    return authorization_code

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result



'''
This returns a list of dictionaries that contains information about each artist
'''
def getTop5Artists(token):
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = get_auth_header(token)

    params = {
      #  "time_range": "medium_term", default is medium term so we don't have to include
        "limit": 5
    }
    result = get(url, headers=headers, params=params)
    if result.status_code == 200:
        top_artists = json.loads(result.content)["items"]
        return top_artists
    else:
        print(f"Error {result.status_code}: {result.text}")
        return None

#not needed anymore?  
def getTop2ArtistIDs(top5Artists):
    artist_ids = [artist["id"] for artist in top5Artists]
    return artist_ids

'''
This takes in a dictionary of all the artists and their informaiton
'''
def getTop5GenresFromArtist(top5Artists):
    artist_genres = [genres ["genres"] for genres in top5Artists]
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
    for i in range (2):
        topGenre = sortedTupleFrequency[i][0]
        finalGenres.append(topGenre)

    return finalGenres

def makeRecommendationPlaylist(token):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    top5Genres = getTop5GenresFromArtist(getTop5Artists(token))
    params = {
        'market' : 'uS',
        'seed_genres' : top5Genres
    }

    result = get(url, headers=headers, params=params)

    
if __name__ == "__main__":
    dict = {"song 1" : 3, "song 2" : 1, "song 3" : 2}
    tuple = tuple(dict.items())
    
'''
token = get_token()
result = search_for_artist(token, "KALI UCHIS")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
   print(f"{idx + 1}. {song['name']}")

getTop10Artists(token)
'''
'''
if __name__ == "__main__":
    authorization_code = get_authorization_code()

    # Exchange authorization code for access token
    access_token = get_token()

    # Access user's top artists using the obtained access token
    top_artists = getTop10Artists(access_token)

    # Display top artists
    if top_artists:
        print("Your Top 10 Artists:")
        for idx, artist in enumerate(top_artists, start=1):
            print(f"{idx}. {artist['name']}")
    else:
        print("Failed to retrieve top artists.")
'''