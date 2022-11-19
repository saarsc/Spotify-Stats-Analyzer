from src.importer import Importer
from src.groupper import Groupper
import src.db as db
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from src.utils import sort_by_date

data = Importer().import_data()
groupper = Groupper(data)
groupper.by_song_key()

grouped_songs = groupper.data

songs_metdata = {
  song.song_key: song
  for song in db.by_keys(grouped_songs.keys())
}

for key, songs in grouped_songs.items():
  metadata = songs_metdata[key]
  for song in songs:
    song.metadata = metadata.get_metadata()
  data += songs

groupper.raw_data = data
groupper.group_by_month()
grouped_songs = groupper.data

data = {}

for time_period, songs in grouped_songs.items():
  songs = sort_by_date("date", songs)
  values = [
    song.metadata["danceability"]
    for song in songs
  ]
  time_periods = [
    song.timestamp
    for song in songs
  ]

  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
  plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
  plt.plot(time_periods, values, label=time_period)

plt.legend()
plt.show()
print()
