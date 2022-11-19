from ..song import Song
class BaseClassifier:
  def __init__(self, data: list[Song]) -> None:
    self.data = data
  
  def classifiy_songs(self):
    return [
      {
        **song.as_row(),
        **self._classifiy_song(song)
      }
      for song in self.data
    ]
    

  def _classifiy_song(self, song: Song) -> dict:
    raise NotImplementedError