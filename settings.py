from tinydb import TinyDB

_db = TinyDB('db.json')
db_popular = _db.table("popular")
db_movies = _db.table("movies")

POPULARITY_PROVIDER = "providers.popularity.torrentz"
MOVIEDATA_PROVIDERS = [
    "providers.moviedata.filmtipset",
    "providers.moviedata.imdb",
]
OUTPUT_PROVIDER = "providers.output.terminal"

from access_keys import ACCESS_KEYS  # NOQA
