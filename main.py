import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
SPOTIFY_DISPLAY_NAME = ""

user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/" + user_date
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
all_songs = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
all_songs_list = [song.getText().strip() for song in all_songs]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_DISPLAY_NAME,
    )
)
user_id = sp.current_user()["id"]


# Searching Spotify for songs by title
song_uris = []
year = user_date.split("-")[0]

for song in all_songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)
print(playlist)


# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
