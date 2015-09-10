import re
from application import APPLICATION as APP

def clear_cache(name):
    APP.debug("Clearing %s from movie db..." % name)
    name_str = " ".join(re.split(r"[^\w'-:]+", name)).lower()
    imdb_id = APP.NameMapper.get_id(name_str)
    if not imdb_id:
        APP.output("Found no movie named \"%s\"" % name)
        return

    APP.debug("Found matching IMDB id %s..." % imdb_id)
    APP.Movie.remove_id(imdb_id)

def main(arguments):
    APP.settings["DEBUG"] = arguments["--debug"]

    name = arguments["<name>"]
    clear_cache(name)
