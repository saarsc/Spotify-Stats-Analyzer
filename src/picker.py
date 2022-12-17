from .groupper import Groupper
from .song import Song
from .db.tables.song_entrie import SongEntrie
from .db import db
from .classifier.time_classifier import TimeClassifier

class Picker:
  def __init__(self, data: list[Song]) -> None:
    self.data = data
  
  def process_data(self):
    songs = self._map_song_stats()
    songs = TimeClassifier(songs).classifiy_songs()
    return songs
  
  def _map_song_stats(self) -> list[Song]:
    groupper = Groupper(self.data)
    groupped_songs = groupper.by_song_key()
    songs_metdata:list[SongEntrie] = {
      song.song_key: song
      for song in db.by_keys(groupped_songs.keys())
    }
    data = []
    for key, songs in groupped_songs.items():
      metadata = songs_metdata[key]
      for song in songs:
        song.metadata = metadata.get_metadata()
      data += songs
    
    return data