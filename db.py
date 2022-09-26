from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from song import Song
from song_entrie import SongEntrie

conn = create_engine("sqlite:///songs.db", echo=True)
session = sessionmaker(bind=conn)()

def insert_rows(rows: list[Song]): 
  session.add_all([SongEntrie(**row.as_row()) for row in rows])
  session.commit()

def by_key(key):
  return session.query(SongEntrie).filter(SongEntrie.song_key == key).first()

def by_keys(keys):
  return session.query(SongEntrie.song_key).filter(SongEntrie.song_key.in_(list(keys))).all()

def existing_keys():
  return session.query(SongEntrie.song_key).all()

def insert_row(row: Song):
  session.add(SongEntrie(**row.as_row()))
  session.commit()
