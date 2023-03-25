from functools import cached_property
import hashlib
from datetime import datetime
from typing import Union
from .db.tables.album_table import Album 
from .db.tables.artist_table import Artist 
class Song():
  def __init__(self, name: str="", album: str="", artist: str="", timestamp:str="", spotify_id:str=None, **kwargs) -> None:
    self.name: str = name
    self.album: Union[Album, str] = album or name
    self.artist: Union[Artist, str] = artist
    try:
      self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
      self.timestamp = timestamp
    self._metadata = {}
    self.spotify_id = spotify_id

  @cached_property
  def query(self) -> str:
    return f"track:{self.name} artist:{self.artist} album:{self.album}".replace("'", "")
  
  @cached_property
  def simple_query(self):
    return f"track:{self.name} artist:{self.artist}".replace("'", "")

  @property
  def key(self) -> str:
    return hashlib.md5(self.query.encode()).hexdigest()

  @property
  def metadata(self):
    return {
      "danceability": self._metadata.get("danceability"),
      "energy": self._metadata.get("energy"),
      "key": self._metadata.get("key"),
      "loudness": self._metadata.get("loudness"),
      "mode": self._metadata.get("mode"),
      "speechiness": self._metadata.get("speechiness"),
      "acousticness": self._metadata.get("acousticness"),
      "instrumentalness": self._metadata.get("instrumentalness"),
      "liveness": self._metadata.get("liveness"),
      "valence": self._metadata.get("valence"),
      "tempo": self._metadata.get("tempo"),
      "duration_ms": self._metadata.get("duration_ms"),
      "time_signature": self._metadata.get("time_signature")    
    }
  
  @metadata.setter
  def metadata(self, value):
    self._metadata = value

  def as_row(self) -> dict:
    return {
      "song_key": self.key,
      "artist": self.artist,
      "album": self.album,
      "name": self.name,
      "spotify_id": self.spotify_id,
      **self.metadata
    }
  
  def __repr__(self) -> str:
    return self.query

  def __eq__(self, other) -> bool:
    if isinstance(other, Song):
      return (self.key == other.key)
    else:
      return False 

  def __hash__(self) -> int:
    return hash(self.key)
  
  def __getitem__(self, key):
    return self.__getattribute__(key)
  
  def __add__(self, other) -> dict:
    song = Song()
    if (isinstance(other, Song)):
      song.metadata = {
        k: (self.metadata.get(k) or 0) + (other.metadata.get(k) or 0)
        for k in self.metadata
      }
    else:
      song.metadata = {
        k: (self.metadata.get(k) or 0) + (other["metadata"].get(k) or 0)
        for k in self.metadata
      }
    return song
  
  def to_dict(self):
    return {
      **self.metadata,
      "artist": self.artist.as_dict(),
      "album": self.album.as_dict()
    }
