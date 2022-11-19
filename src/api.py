import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.creds import *
from src.song import Song
from termcolor import colored
import src.utils as utils
import src.db as db
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
      db.insert_row(song)
      print(colored(f"{song.query} not found", "red"))
    # TODO: 
    # Need to rewrite this to one API call.
    # So Search by name -> filter results by artist -> by album.
    try:
      result = self.sp.search(song.query)
      assert result["tracks"]["items"][0]
    except:
      try:
        result = self.sp.search(song.simple_query)
        assert result["tracks"]["items"][0]
      except:
        try:
          result = self.sp.search(song.name)
        except:
          save_invalid_song(song)
          return None

        item = [
          item
          for item in result["tracks"]["items"]
          if item["artists"][0]["name"] == song.artist or item["album"]["name"] == song.album
        ]
          
        result["tracks"]["items"] = item
  
    try: 
      id = result["tracks"]["items"][0]['id']
      song.spotify_id = id
      return id
    except IndexError:
      save_invalid_song(song)

  def get_songs_features(self, songs: list[Song]):
    in_db:list[str] = [
      key[0]
      for key in db.existing_keys()
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

      db.insert_rows(chunk)
      
      
    songs = [song for chunk in chunks for song in chunk]
    
    return self.cache