from tinydb import TinyDB

_db = TinyDB('db.json')
db_popular = _db.table("popular")
db_movies = _db.table("movies")

POPULARITY_PROVIDER = "providers.popularity.torrentz"
MOVIEDATA_PROVIDERS = [
    # "providers.moviedata.imdb",
    "providers.moviedata.filmtipset",
]

from access_keys import ACCESS_KEYS  # NOQA
