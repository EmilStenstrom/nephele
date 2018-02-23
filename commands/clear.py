from importlib import import_module

from application import APPLICATION as APP
from utils.torrent_util import torrent_to_movie


def clear_cache(name):
    APP.debug("Clearing \"%s\" from movie db..." % name)
    movie = torrent_to_movie(name)
    record = APP.Movie.get_data(movie)

    if not record:
        APP.output("Could not find movie in db: %s" % name)
        return

    clear_webcache(record)

    APP.output("Deleted movie from database: %s" % record["title"])
    APP.Movie.remove("id", record["id"])

def clear_webcache(movie):
    for provider_path in APP.setting("MOVIEDATA_PROVIDERS"):
        provider_module = import_module(provider_path)
        provider = provider_module.Provider()

        APP.debug("Clearing movie name (%s) from webcache" % movie["title"])
        clear_url(provider.get_url({
            "name": movie["title"].lower()
        }))
        # Make sure we clear URLs with year too
        clear_url(provider.get_url({
            "name": movie["title"].lower(),
            "year": movie["year"],
        }))
        for search_phrase in movie["search_phrases"]:
            APP.debug("Clearing movie search phrase (%s) from webcache" % search_phrase)
            clear_url(provider.get_url({
                "name": search_phrase,
            }))
            # Make sure we clear URLs with year too
            clear_url(provider.get_url({
                "name": search_phrase,
                "year": movie["year"],
            }))

def clear_url(url):
    cached_session = APP.setting("WEBCACHE")
    if cached_session.cache.has_url(url):
        cached_session.cache.delete_url(url)
        APP.output("Deleted url from webcache: %s" % url)
    else:
        APP.debug("Found no match for %s in webcache." % url)

def main(arguments):
    APP.settings["DEBUG"] = arguments["--debug"]

    name = arguments["<name>"]
    clear_cache(name)
