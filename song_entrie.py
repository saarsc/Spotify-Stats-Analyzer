from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, String, Integer

Base = declarative_base()

class SongEntrie(Base):
  __tablename__ = "songs"

  id = Column("id", Integer, primary_key= True)
  song_key = Column("song_key", String)
  artist = Column("artist", String)
  album = Column("album", String)
  name = Column("name", String)
  danceability = Column("danceability", Float)
  energy = Column("energy", Float)
  key = Column("key", Float)
  loudness = Column("loudness", Float)
  mode = Column("mode", Float)
  speechiness = Column("speechiness", Float)
  acousticness = Column("acousticness", Float)
  instrumentalness = Column("instrumentalness", Float)
  liveness = Column("liveness", Float)
  valence = Column("valence", Float)
  tempo = Column("tempo", Float)
  duration_ms = Column("duration_ms", Float)
  time_signature = Column("time_signature", Float)
  spotify_id = Column("spotify_id", String)
