from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

def get_token():
    #concatenating the id and secret and encode it into a base 64
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    #HTTP Request to the spotify authorization service
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }

    data = {"grant_type": "client_credentials",
            "scope": "user-top-read,"}

    #formulate the POST request
    result = post(url, headers = headers, data = data)

    #convert a json result into a python dictionary
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


#for any future requests
def get_auth_header(token):
    return {"Authorization":"Bearer " + token}


#search for an artist
def search_for_artists(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query =f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("no artists with this name exists...")
        return None
    return json_result[0]
    
def get_songs_by_artist(token, artist_id, country):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_my_top_items(token, type):
    url = f"https://api.spotify.com/v1/me/top/{type}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)

    if result.status_code != 200:
        print("Error accessing the API. Status code:", result.status_code)
        print("API Response Content:", result.content)
        print("API Response Headers:", result.headers)
        return []

    try:
        json_result = json.loads(result.content)["items"]
        return json_result
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        print("API Response:", result.text)
        return []

    
def get_artist_correlation(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)['artists']
    return json_result

def get_followed_artists():
    url = f"https://api.spotify.com/v1/me/following"



###################################################################################





#token we will use to request any information we need from the API
token = get_token()
print(token)
result = search_for_artists(token, "Queen")
print(result["name"])
artists_id = result["id"]
songs = get_songs_by_artist(token, artists_id, 'US')
#top_artists = get_my_top_items(token, "artists")
artist = search_for_artists(token, "Bruno Mars")
correlations = get_artist_correlation(artist["id"])
for song in songs:
    print(song['name'])

for a in correlations:
    print(a['name'])



