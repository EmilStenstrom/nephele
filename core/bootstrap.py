from __future__ import print_function
from tinydb import TinyDB
from core.models import NameMapper, Movie

TABLE_POPULAR = "popular"
TABLE_NAME_TO_ID = "name_to_id_mapping"
TABLE_MOVIES = "movies"

class Application(object):
    def __init__(self, settings):
        database = TinyDB(settings["DATABASE"])
        self.NameMapper = NameMapper(database, TABLE_NAME_TO_ID)
        self.Movie = Movie(database, TABLE_MOVIES)

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
