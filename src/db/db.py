from typing import Union
from src.song import Song
 
from .tables.song_entrie import SongEntrie
from .tables.artist_table import Artist
from .tables.album_table import Album

from .db_config import session

SONGS_TABLE = SongEntrie(session=session)
ARTIST_TABLE = Artist(session=session)
ALBUM_TABLE = Album(session=session)

SONGS_TABLE.metadata.create_all()

def existing_songs_keys():
  return SONGS_TABLE.existing_keys()

def insert_song(song: Song):
  insert_songs([song])

def populate_artist_and_album(func):
  def populate(songs: list[Song]):
    # TODO: 
    # To save DB hits should be groupped that way we'd only run on query
    for song in songs:
      song.artist = find_or_create_artist(song)
      song.album = find_or_create_album(song)
    
    func(songs)

  return populate

@populate_artist_and_album
def insert_songs(songs: list[Song]):
  SONGS_TABLE.insert_rows(songs)

def find_or_create_album(song: Song) -> Album:
  return find_or_create(ALBUM_TABLE, name=song.album, artist=song.artist)

def find_or_create_artist(song: Song) -> Artist:
  return find_or_create(ARTIST_TABLE, name=song.artist)

def find_or_create(table: Union[Artist, SongEntrie, Album], **kwargs) -> Union[SongEntrie, Album, Artist]:
  return table.find_or_create_by_name(**kwargs)

def insert_stats():
  ARTIST_TABLE.calculate_stats()
  ALBUM_TABLE.calculate_stats()

insert_stats()