from api import SpotifyApi
from  pprint import pprint
from importer import Importer

importer = Importer()
data = importer.import_data()
api = SpotifyApi()

pprint(api.get_songs_features(data))

api.export_songs_cache()