import re

from application import ACCESS_KEYS
from application import APPLICATION as APP
from providers.moviedata.provider import MoviedataProvider

IDENTIFIER = "OMDb"

class Provider(MoviedataProvider):
    def __init__(self):
        if IDENTIFIER not in ACCESS_KEYS or not ACCESS_KEYS[IDENTIFIER]:
            raise SystemExit("APIKEY for {} not found in access_keys.py.".format(IDENTIFIER))

        super(Provider, self).__init__()

    def get_url(self, movie):
        parameters = {
            "t": movie["name"].encode("utf-8"),
            "apikey": ACCESS_KEYS[IDENTIFIER]["APIKEY"],
        }
        if "year" in movie and movie["year"]:
            parameters["y"] = movie["year"]

        return "https://www.omdbapi.com/?" + self.urlencode(parameters)

    def fetch_movie_data(self, movie):
        url = self.get_url(movie)
        APP.debug("Fetching url: %s" % url)
        data = self.parse_json(url)
        if not data or data["Response"] == "False":
            return {}

        return self.transform_data(data)

    def get_data_mapping(self):
        return {
            "id": "imdbID",
            "title": "Title",
            "plot": "Plot",
            "genre": lambda data: data.get("Genre", "").split(", "),
            "director": lambda data: data.get("Director", "").split(", ")[0] if data.get("Director") else "",
            "country": lambda data: data.get("Country", "").split(", "),
            "language": lambda data: data.get("Language", "").split(", "),
            "runtime": "Runtime",
            "released": "Released",
            "age_rating": "Rated",
            "year": "Year",
            "metacritic_rating": "Metascore",
            "imdb_url": lambda data: "https://www.imdb.com/title/" + data.get("imdbID"),
            "imdb_poster": "Poster",
            "imdb_rating": "imdbRating",
        }
