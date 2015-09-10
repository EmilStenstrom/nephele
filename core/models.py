from tinydb import where

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

class NameMapper(Model):
    def get_id(self, name):
        record = self.find("name", name)
        if record:
            return record["id"]

        return None

    def update_mapping(self, name, provider):
        imdb_id, data = provider.get_movie_data(name)
        if not imdb_id:
            return

        self.insert({"name": name, "id": imdb_id})

class Movie(Model):
    def get_data(self, imdb_id, provider):
        if not imdb_id:
            return None

        record = self.find("id", imdb_id)
        if record:
            mapping = provider.get_data_mapping()
            has_all_keys = True
            for key in mapping.keys():
                if key not in record:
                    has_all_keys = False
                    break

            if has_all_keys:
                return record

            return None

        return None

    def update_movie(self, name, provider):
        imdb_id, data = provider.get_movie_data(name)

        if data:
            self.insert_or_update("id", imdb_id, data)

        return imdb_id, data
