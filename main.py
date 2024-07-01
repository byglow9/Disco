from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

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

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    
    if "artists" in json_result and "items" in json_result["artists"]:
        artists = json_result["artists"]["items"]
        if len(artists) > 0:
            return artists[0]  # Retorna o primeiro artista encontrado
        else:
            print("No artist with this name exists...")
            return None
    else:
        print("Unexpected response format from Spotify API")
        return None
    
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    
    if "tracks" in json_result:
        return json_result["tracks"]
    else:
        print("No tracks found for this artist...")
        return None

def print_song_names(songs):
    if songs:
        print("Top Tracks:")
        for i, song in enumerate(songs):
            print(f"{i+1}. {song['name']}")
    else:
        print("No songs available.")

token = get_token()
result = search_for_artist(token, "Glowboy ✨")
if result:
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    print_song_names(songs)
