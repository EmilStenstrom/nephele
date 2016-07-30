from importlib import import_module
from application import APPLICATION as APP
from utils.movie_util import update_moviedata

def get_popular():
    APP.debug("Fetching popular movies...")
    provider_module = import_module(APP.setting("POPULARITY_PROVIDER"))
    provider = provider_module.Provider()
    APP.debug("Fetching from %s" % provider_module.IDENTIFIER)
    return provider.get_popular()

def output(movie_data):
    provider_module = import_module(APP.setting("OUTPUT_PROVIDER"))
    provider = provider_module.Provider()
    APP.debug("Outputting data with %s" % provider_module.IDENTIFIER)
    provider.output(movie_data)

def main(arguments):
    APP.settings["DEBUG"] = arguments["--debug"]

    popular = get_popular()
    update_moviedata(popular, APP)

    records = []
    for movie in popular:
        data = APP.Movie.get_data(movie)
        if not data or data in records:
            continue

        records.append(data)

    output(records)
