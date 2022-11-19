from functools import reduce
from itertools import groupby
from typing import Union
from src.song import Song
from src.utils import prepare_list_for_group

class Groupper():
  def __init__(self, data: list[Song]) -> None:
    self.raw_data: Union[list[Song], dict] = data
  
  @property
  def data(self) -> dict:
    return {k:list(v) for k, v in self._data}

  @prepare_list_for_group(time_period="week")
  def group_by_week(self) -> dict:
    self._data = groupby(self.raw_data, lambda s: s.timestamp.isocalendar().week)
    return self.data

  @prepare_list_for_group(time_period="weekday")
  def group_by_weekday(self) -> dict:
    self._data = groupby(self.raw_data, lambda s: s.timestamp.isocalendar().weekday)
    return self.data
  
  @prepare_list_for_group
  def group_by_year(self) -> dict:
    self._data = groupby(self.raw_data, lambda s: s.timestamp.isocalendar().year)
    return self.data
  
  @prepare_list_for_group(time_period="month")
  def group_by_month(self) -> dict:
    self._data = groupby(self.raw_data, lambda s: s.timestamp.month)
    return self.data
  
  def sum_values(self):
    for time_period, val in self.raw_data.items():
      t = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), val)
  
  def by_song_key(self):
    self.raw_data.sort(key= lambda x: x.key)
    self._data = groupby(self.raw_data, lambda x: x.key)
    return self.data

