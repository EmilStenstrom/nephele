from __future__ import print_function
import os
from importlib import import_module
from application import APPLICATION as APP
from utils.torrent_util import torrent_to_search_string, remove_bad_torrent_matches
from utils.movie_util import update_moviedata

def is_proper_movie_file(filename, is_directory):
    FILE_ENDINGS = [".mkv", ".mp4", ".avi", ".iso", ".mov", ".mpeg"]
    # Proper filenames
    for ending in FILE_ENDINGS:
        if filename.endswith(ending):
            return True

    # Not stuff that ends with "-ignore"
    if filename.endswith("-ignore"):
        return False

    # Only directories left
    if is_directory:
        return True

    return False

def get_filenames(directory):
    APP.debug("Loading movies from: %s" % directory)
    files = os.listdir(directory)
    files = [(filename, os.path.isdir(os.path.join(directory, filename))) for filename in files]
    movies = [filename for filename, is_directory in files if is_proper_movie_file(filename, is_directory)]
    return movies

def output(movie_data):
    provider_module = import_module(APP.setting("OUTPUT_PROVIDER"))
    provider = provider_module.Provider()
    APP.debug("Outputting data with %s" % provider_module.IDENTIFIER)
    provider.output(movie_data)

def main(arguments):
    APP.settings["DEBUG"] = arguments["--debug"]
    directory = arguments["<directory>"]

    movies = get_filenames(directory)
    movies = [torrent_to_search_string(name) for name in movies]
    movies = remove_bad_torrent_matches(movies)

    update_moviedata(movies, APP)
    records = APP.Movie.all()
    output(records)
