import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.creds import *
from src.song import Song
from termcolor import colored
import src.utils as utils
from .db.db import insert_song, insert_songs, existing_songs_keys, find_or_create_album
from typing import *

class SpotifyApi():
  def __init__(self, load_cache=True) -> None:
    auth_manger = SpotifyClientCredentials(
      client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_SECRET
    )
    self.sp = spotipy.Spotify(
      auth_manager=auth_manger
    )

  def get_song_id(self, song: Song) -> str:
    """
      Trying to search for the Spotify song ID by using a less strict query each time if the song cannot be found
    """
    def save_invalid_song(song: Song):
      song.metadata = {
        "spotify_id": None
      }
      insert_song(song)
      print(colored(f"{song.query} not found", "red"))

    def locate_song(item: dict) -> bool:
      return (
        [
          artist["name"].lower() == song.artist.lower()
          for artist in item["artists"]
        ] or
        song.album.lower() in item["album"]["name"].lower()
      )

    try:
      item = None
      for query in [song.name, song.simple_query, song.query]:
        result = self.sp.search(query)
        if items := result.get("tracks", {}).get("items"):
          item = list(filter(locate_song, items))
          if item:
            break

      assert item, Exception(f"Song #{song.name} not found")

      id = item[0]['id']
      song.spotify_id = id
      return id
    except:
      save_invalid_song(song)

  def get_songs_features(self, songs: list[Song]):
    in_db:list[str] = [
      key[0]
      for key in existing_songs_keys()
    ]
    chunks:Generator[list[Song]] = utils.split_to_chunks([
      song for song in set(songs)
      if song.key not in in_db
    ], 100)

    for chunk in chunks:
      ids = [
        self.get_song_id(song)
        for song in chunk
      ]
      ids = list(
        filter(
          lambda id: id is not None, ids
        )
      )
      result = self.sp.audio_features(ids)
      for i, r in enumerate(result):
        song = chunk[i]
        song.metadata = r or {}

      insert_songs(chunk)


    songs = [song for chunk in chunks for song in chunk]

    return self.cache
