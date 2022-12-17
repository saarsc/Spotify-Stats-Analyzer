from typing import Any
from sqlalchemy.orm import relationship, Session
from .stats_based_table import StatsBasedTable
from ..db_config import Base

class Artist(StatsBasedTable, Base):
  __tablename__ = "artist"

  albums = relationship("Album", back_populates="artist")
  songs = relationship("SongEntrie", back_populates="artist")