from importlib import import_module
from application import APPLICATION as APP

def get_popular(debug=False):
    APP.debug("Fetching popular movies...")
    record = APP.Popular.find("key", "popular")
    if not record:
        provider_module = import_module(APP.setting("POPULARITY_PROVIDER"))
        provider = provider_module.Provider(debug=debug)
        APP.debug("Fetching from %s" % provider_module.IDENTIFIER)
        popular = provider.get_popular()
        APP.Popular.insert({"key": "popular", "value": popular})
    else:
        APP.debug("Found result popular_db")

def get_moviedata(popular_list, debug=False):
    def get_id_from_name(name):
        record = APP.Name_to_id.find("name", name)
        if record:
            return record["id"]

        return None

    def get_data_from_id(imdb_id, provider):
        if not imdb_id:
            return None

        record = APP.Movie.find("id", imdb_id)
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
            APP.Name_to_id.insert({"name": name, "id": imdb_id})

        if data:
            APP.Movie.insert_or_update("id", imdb_id, data)

        return imdb_id, data

    for name in popular_list:
        imdb_id = get_id_from_name(name)

        for provider_path in APP.setting("MOVIEDATA_PROVIDERS"):
            provider_module = import_module(provider_path)
            provider = provider_module.Provider(debug=debug)
            data = get_data_from_id(imdb_id, provider)
            if imdb_id and data:
                APP.debug_or_dot("Found result in movie db: " + imdb_id)
            else:
                APP.debug_or_dot("Fetching from %s" % provider_module.IDENTIFIER)
                _, data = update_mapping_and_movie_db(name, provider)

def output(movie_data, debug=False):
    provider_module = import_module(APP.setting("OUTPUT_PROVIDER"))
    provider = provider_module.Provider(debug=debug)
    APP.debug("Outputting data with %s" % provider_module.IDENTIFIER)
    provider.output(movie_data)

def main(arguments):
    debug = "debug" in arguments
    get_popular(debug=debug)

    records = APP.Popular.all()
    get_moviedata(records[0]["value"], debug=debug)

    records = APP.Movie.all()
    output(records, debug=debug)
