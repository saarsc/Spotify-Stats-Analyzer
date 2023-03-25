from ..song import Song
from ..db.tables.song_entrie import SongEntrie
class BaseClassifier:
  def __init__(self, data: list[SongEntrie]) -> None:
    self.data = data
  
  def classifiy_songs(self):
    return [
      {
        **song.to_dict(),
        **self._classifiy_date(song),
      }
      for song in self.data
    ]
    
  def _classifiy_date(self, song: Song): 
    if timestamp := song.timestamp:
      return {
        "minute": timestamp.minute,
        "hour": timestamp.hour,
        "weekday": timestamp.weekday(),
        "week": timestamp.isocalendar().week,
        "day": timestamp.day,
        "month": timestamp.month
      }