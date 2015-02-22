from __future__ import print_function
import sys
from tinydb import where
from importlib import import_module
from settings import (
    POPULARITY_PROVIDER, MOVIEDATA_PROVIDERS, OUTPUT_PROVIDER,
    db_popular, db_movies, db_name_to_id_mapping
)

def get_popular(debug=False):
    print("Fetching Popular:")
    record = db_popular.get(where("key") == "popular")
    if not record:
        provider_module = import_module(POPULARITY_PROVIDER)
        provider = provider_module.Provider(debug=debug)
        print("Fetching from %s" % provider_module.IDENTIFIER)
        popular = provider.get_popular()
        db_popular.insert({"key": "popular", "value": popular})
    else:
        print("Found result popular_db")

def get_moviedata(popular_list, debug=False):
    def get_id_from_name(name):
        record = db_name_to_id_mapping.get(where("name") == name)
        if record:
            return record["id"]

        return None

    def get_data_from_id(imdb_id, provider):
        if not imdb_id:
            return None

        record = db_movies.get(where("id") == imdb_id)
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

    def update_mapping_and_movie_db(name, provider):
        imdb_id, data = provider.get_movie_data(name)

        if imdb_id:
            db_name_to_id_mapping.insert({"name": name, "id": imdb_id})

        if data:
            record = db_movies.get(where("id") == imdb_id)
            if record:
                # Never overwrite existing data
                new_data = {key: value for key, value in data.items() if key not in record}
                db_movies.update(new_data, where("id") == imdb_id)
            else:
                db_movies.insert(data)

        return imdb_id, data

    for name in popular_list:
        imdb_id = get_id_from_name(name)

        for provider_path in MOVIEDATA_PROVIDERS:
            provider_module = import_module(provider_path)
            provider = provider_module.Provider(debug=debug)
            data = get_data_from_id(imdb_id, provider)
            if imdb_id and data:
                print("Found result in movie db:", imdb_id)
            else:
                print("Fetching from %s" % provider_module.IDENTIFIER)
                _, data = update_mapping_and_movie_db(name, provider)

def output(movie_data):
    provider_module = import_module(OUTPUT_PROVIDER)
    provider = provider_module.Provider(debug=debug)
    print("Outputting data with %s" % provider_module.IDENTIFIER)
    provider.output(movie_data)

def main(debug=False):
    get_popular(debug=debug)

    records = db_popular.all()
    get_moviedata(records[0]["value"], debug=debug)

    records = db_movies.all()
    output(records)

# Usage:
# python get_popular.py
# python get_popular.py --verbose
if __name__ == "__main__":
    debug = False
    if len(sys.argv) == 2:
        if sys.argv[1] == "--verbose":
            debug = True

    main(debug=debug)
