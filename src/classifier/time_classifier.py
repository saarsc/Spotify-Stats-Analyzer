from datetime import datetime
from .base_classifier import BaseClassifier
from ..song import Song
class TimeClassifier(BaseClassifier):
  def __init__(self, data: list[Song]) -> None:
    super().__init__(data)

  def _classifiy_song(self, song: Song):
    timestamp = song.timestamp
    return {
      "minute": timestamp.minute,
      "hour": timestamp.hour,
      "weekday": timestamp.weekday(),
      "week": timestamp.isocalendar().week,
      "day": timestamp.day,
      "month": timestamp.month
    }