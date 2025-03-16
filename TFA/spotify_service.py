import requests

def get_spotify_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=payload, auth=(client_id, client_secret))
    return response.json().get('access_token', None)

def search_tracks(query, token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": 10
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


