from flask import Flask, send_from_directory, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)
CORS(app)  # Adiciona suporte a CORS

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
            return None
    else:
        return None

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    
    if "tracks" in json_result:
        return [track["name"] for track in json_result["tracks"]]
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    try:
        artist_name = request.args.get('artist_name')
        if not artist_name:
            return jsonify({'error': 'No artist name provided'}), 400
        
        token = get_token()
        artist = search_for_artist(token, artist_name)
        if not artist:
            return jsonify({'error': 'Artist not found'}), 404
        
        artist_id = artist['id']
        songs = get_songs_by_artist(token, artist_id)
        if not songs:
            return jsonify({'error': 'No songs found for this artist'}), 404
        
        return jsonify({'songs': songs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
