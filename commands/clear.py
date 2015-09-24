from importlib import import_module
from utils.torrent_util import torrent_to_movie
from application import APPLICATION as APP
import platform

def clear_cache(name):
    if platform.system() == 'Windows':
        name = name.decode("windows-1252")

    APP.debug("Clearing \"%s\" from movie db..." % name)
    movie = torrent_to_movie(name)
    clear_webcache(movie)

    record = APP.Movie.get_data(movie)

    if not record:
        APP.output("Could not find movie in db: %s" % name)
        return

    # Querying with and without year can give different URLs
    if not movie["year"] and record["year"]:
        movie["year"] = record["year"]
        clear_webcache(movie)

    APP.output("Deleted movie from database: %s" % record["title"])
    APP.Movie.remove("id", record["id"])

def clear_webcache(movie):
    cached_session = APP.setting("WEBCACHE")
    for provider_path in APP.setting("MOVIEDATA_PROVIDERS"):
        provider_module = import_module(provider_path)
        provider = provider_module.Provider()
        url = provider.get_url(movie)
        if cached_session.cache.has_url(url):
            cached_session.cache.delete_url(url)
            APP.output("Deleted url from webcache: %s" % url)

def main(arguments):
    APP.settings["DEBUG"] = arguments["--debug"]

    name = arguments["<name>"]
    clear_cache(name)
