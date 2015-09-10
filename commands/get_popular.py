from importlib import import_module
from application import APPLICATION as APP

def get_popular():
    APP.debug("Fetching popular movies...")
    provider_module = import_module(APP.setting("POPULARITY_PROVIDER"))
    provider = provider_module.Provider()
    APP.debug("Fetching from %s" % provider_module.IDENTIFIER)
    return provider.get_popular()

def update_moviedata(popular_list):
    for name in popular_list:
        imdb_id = APP.NameMapper.get_id(name)

        for provider_path in APP.setting("MOVIEDATA_PROVIDERS"):
            provider_module = import_module(provider_path)
            provider = provider_module.Provider()
            data = APP.Movie.get_data(imdb_id, provider)
            if imdb_id and data:
                APP.debug_or_dot("Found result in movie db: " + imdb_id)
            else:
                APP.debug_or_dot("Fetching from %s" % provider_module.IDENTIFIER)
                APP.NameMapper.update_mapping(name, provider)
                APP.Movie.update_movie(name, provider)

def output(movie_data):
    provider_module = import_module(APP.setting("OUTPUT_PROVIDER"))
    provider = provider_module.Provider()
    APP.debug("Outputting data with %s" % provider_module.IDENTIFIER)
    provider.output(movie_data)

def main(arguments):
    APP.settings["DEBUG"] = arguments["--debug"]

    popular = get_popular()
    update_moviedata(popular)
    records = APP.Movie.all()
    output(records)
