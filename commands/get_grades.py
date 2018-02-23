import os
from importlib import import_module

from application import APPLICATION as APP
from utils.movie_util import update_moviedata
from utils.torrent_util import remove_bad_torrent_matches, torrent_to_movie


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

def output(movie_data, limit, filters):
    provider_module = import_module(APP.setting("OUTPUT_PROVIDER"))
    provider = provider_module.Provider()
    APP.debug("Outputting data with %s" % provider_module.IDENTIFIER)
    provider.output(movie_data, limit, filters)

def main(arguments):
    APP.settings["DEBUG"] = arguments["--debug"]
    directory = arguments["<directory>"]

    filenames = get_filenames(directory)
    movies = [torrent_to_movie(name) for name in filenames]
    movies = remove_bad_torrent_matches(movies)

    update_moviedata(movies, APP)

    records = []
    for movie in movies:
        data = APP.Movie.get_data(movie)
        if not data or data in records:
            continue

        records.append(data)

    output(records, int(arguments["--limit"]), arguments["--filter"])
