from __future__ import print_function
from tinydb import TinyDB, where

TABLE_POPULAR = "popular"
TABLE_NAME_TO_ID = "name_to_id_mapping"
TABLE_MOVIES = "movies"

class Application(object):
    def __init__(self, settings):
        database = TinyDB(settings["DATABASE"])
        self.Popular = Model(database, TABLE_POPULAR)
        self.Name_to_id = Model(database, TABLE_NAME_TO_ID)
        self.Movie = Model(database, TABLE_MOVIES)

        self.settings = settings

    def setting(self, key):
        return self.settings[key]

    def debug(self, message):
        if self.settings.get("DEBUG", False):
            print(message)

    def output(self, message):
        print(message)

    def debug_or_dot(self, message):
        if self.settings.get("DEBUG", False):
            print(message)
        else:
            print(".", end="")

class Model(object):
    def __init__(self, database, table):
        self.table = database.table(table)

    def find(self, key, value):
        return self.table.get(where(key) == value)

    def insert(self, data_dict):
        return self.table.insert(data_dict)

    def update(self, key, value, data_dict):
        return self.table.update(data_dict, where(key) == value)

    def insert_or_update(self, key, value, data_dict):
        record = self.find(key, value)
        if record:
            # Never overwrite existing data
            new_data = {key: value for key, value in data_dict.items() if key not in record}
            return self.update(key, value, new_data)
        else:
            return self.insert(data_dict)

    def all(self):
        return self.table.all()
