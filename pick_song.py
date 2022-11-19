from src.picker import Picker
from src.importer import Importer

data = Importer().import_data()
picker = Picker(data)
songs = picker.process_data()
