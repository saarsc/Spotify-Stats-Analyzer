from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.song import Song
from src.song_entrie import SongEntrie

conn = create_engine("sqlite:///songs.db", echo=True)
session = sessionmaker(bind=conn)()

def insert_rows(rows: list[Song]) -> None: 
  session.add_all([SongEntrie(**row.as_row()) for row in rows])
  session.commit()

def by_key(key) -> SongEntrie:
  return session.query(SongEntrie).filter(SongEntrie.song_key == key).first()

def by_keys(keys) -> list[SongEntrie]:
  return session.query(SongEntrie).filter(SongEntrie.song_key.in_(list(keys))).all()

def existing_keys() -> list[SongEntrie]:
  return session.query(SongEntrie.song_key).all()

def insert_row(row: Song) -> None:
  session.add(SongEntrie(**row.as_row()))
  session.commit()
