from functools import cached_property

from .classifier.base_classifier import BaseClassifier
from .groupper import Groupper
from .song import Song
from .db.tables.song_entrie import SongEntrie
from .db import db

class Picker:
  def __init__(self, data: list[Song]) -> None:
    self.data = data
  
  def process_data(self):
    self.classified_songs
  
  @cached_property
  def classified_songs(self):
    return BaseClassifier(self.songs).classifiy_songs()

  @cached_property
  def songs(self) -> list[Song]:
    groupper = Groupper(self.data)
    groupped_songs = groupper.by_song_key()
    songs_metdata:dict[SongEntrie] = {
      song.song_key: song
      for song in db.by_songs_keys(groupped_songs.keys())
    }

    data:list[Song] = []
    for id, songs in groupped_songs.items():
      if song_info := songs_metdata.get(id):
        for song in songs:
          song.metadata = song_info.get_metadata()
          song.artist = song_info.artist
          song.album = song_info.album
          
        data += songs
    
    return data