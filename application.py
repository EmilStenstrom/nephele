from bootstrap import Application
from access_keys import ACCESS_KEYS  # NOQA

APPLICATION = Application({
    "DATABASE": "db.json",
    "POPULARITY_PROVIDER": "providers.popularity.torrentz",
    "MOVIEDATA_PROVIDERS": [
        "providers.moviedata.filmtipset",
        "providers.moviedata.imdb",
    ],
    "OUTPUT_PROVIDER": "providers.output.terminal",
})
