from src.api import SpotifyApi
from pprint import pprint
from src.importer import Importer
from src.db.db import insert_stats

importer = Importer()
data = importer.import_data()
api = SpotifyApi()

pprint(api.get_songs_features(data))

api.export_songs_cache()

insert_stats()
