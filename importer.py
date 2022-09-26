from contextlib import contextmanager
import csv
import json
from song import Song

class Importer:
  def __init__(self, as_csv=True, filename="out") -> None:
    self.as_csv = as_csv
    self.filename = filename

  def import_csv(self) -> list[Song]:
    with self.data_file() as f:
      reader = csv.DictReader(f, )
      return self.parse_date(reader)
      

  def import_json(self):
    with self.data_file() as f:
      data = json.load(f, )
      return self.parse_date(data)

  def import_db(self):
    raise NotImplementedError

  def import_data(self) -> list[Song]:
    if self.as_csv:
      return self.import_csv()

  @contextmanager
  def data_file(self):
    with open(f"{self.filename}.csv", encoding="utf-8") as f:
      yield f

  def parse_date(self, data: list[dict]) -> list[Song]:
    return [
      Song(**row)
      for row in data
    ]
