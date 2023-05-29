# spotify web scraping project 100 days of code - day 46 hot 100 billboard

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# constants
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
Spotipy_REDIRECT_URI = "https://example.com"
spotify_scope = "playlist-modify-private"
spotify_cache_path = "token.txt"

# get user input
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# scrape billboard top 100
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
song_titles = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_titles = [song.getText() for song in song_titles]

# spotify authentication
client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
redirect_uri = "https://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )

)

user_id = sp.current_user()["id"]

# search spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# create playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# add songs to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

print("Playlist created!")
