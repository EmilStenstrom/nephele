from tinydb import where
from utils.torrent_util import torrent_to_movie

class Model(object):
    def __init__(self, database, table):
        self.table = database.table(table)

    def find(self, key, value):
        return self.table.get(where(key) == value)

    def contains(self, key, value):
        return self.table.contains(where(key) == value)

    def insert(self, data_dict):
        return self.table.insert(data_dict)

    def update(self, key, value, data_dict):
        return self.table.update(data_dict, where(key) == value)

    def update_by_eid(self, eid, data):
        return self.table.update(data, eids=[eid])

    def remove(self, key, value):
        return self.table.remove(where(key) == value)

    def all(self):
        return self.table.all()

class Movie(Model):
    def get_data(self, movie):
        def test_fn(value_list, name):
            return name in value_list

        def equals_clean_movie_name(value, name):
            return torrent_to_movie(value)["name"] == name

        query = (
            where("search_phrases").test(test_fn, movie["name"]) |
            where("title").test(equals_clean_movie_name, movie["name"]) |
            where("title_swe").test(equals_clean_movie_name, movie["name"])
        )
        if movie["year"]:
            query &= (where("year") == movie["year"])

        records = self.table.search(query)

        if not records:
            return None

        return records[0]

    def has_all_fields(self, movie, mapping):
        record = self.get_data(movie)
        if not record:
            return mapping.keys()

        missing_keys = set(mapping.keys()) - set(record.keys())
        return list(missing_keys)

    def update_movie(self, movie, data):
        record = self.find("id", data["id"])

        # Fallback: Sometimes IMDB id's change, use title and year
        if not record:
            record = self.get_data(movie)

        if record:
            data["search_phrases"] = record.get("search_phrases", [])
            if movie["name"] not in data["search_phrases"]:
                data["search_phrases"].append(movie["name"])

            self.update_by_eid(record.eid, data)
        else:
            data["search_phrases"] = [movie["name"]]
            self.insert(data)
