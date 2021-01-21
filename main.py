import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

year = input('Where do you wanna travel to? (Format YYYY-MM-DD)\n')

url = f'https://www.billboard.com/charts/hot-100/{year}'
soup = BeautifulSoup(requests.get(url).text, 'html.parser')
titles =[i.text for i in soup.find_all(class_="chart-element__information__song text--truncate color--primary")]

song_uris = []
for song in titles:
    result = sp.search(q=f'track:{song} year:{year.split("-")[0]}', type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        try:
            result = sp.search(q=f'track:{song}', type="track")
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} not available.")


playlist = sp.user_playlist_create(user=user_id, name=year, public=False, collaborative=False, description="Test Test")
test= sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["uri"], tracks=song_uris, position=None)
