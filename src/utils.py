from typing import Literal
from src.song import Song

TIME_PERIODS = Literal["year", "week", "weekday", "month", "date"]

def split_to_chunks(list: list, chunk_size: int):
  for i in range(0, len(list), chunk_size):
    yield list[i:i + chunk_size]

def sort_by_date(time_period:TIME_PERIODS, list:list[Song]):
  def sort_by_isocalender():
    list.sort(key=lambda s: getattr(s.timestamp.isocalendar(), time_period))

  def sort_by_month():
    list.sort(key=lambda s: s.timestamp.month)

  def sort_by_date():
    list.sort(key=lambda s: s.timestamp)

  SORT_BY_MAPPING = {
    "year": sort_by_isocalender,
    "week": sort_by_isocalender,
    "weekday": sort_by_isocalender,
    "month": sort_by_month,
    "date": sort_by_date,
  }

  SORT_BY_MAPPING[time_period]()

  return list

def prepare_list_for_group(time_period:TIME_PERIODS="year"):
  def sorter(func):
    def sort_by_time_period(*args, **kwargs):
      sort_by_date(time_period, args[0].raw_data)
      func(*args, **kwargs)
      return args[0].raw_data

    return sort_by_time_period

  return sorter
