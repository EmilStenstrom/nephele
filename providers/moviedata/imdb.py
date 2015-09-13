import re
from providers.moviedata.provider import MoviedataProvider
from urllib import urlencode
from application import APPLICATION as APP

IDENTIFIER = "IMDB"

class Provider(MoviedataProvider):
    def get_url(self, movie):
        parameters = {
            "title": movie["name"],
            "limit": 1,
            "filter": "M",
            "format": "JSON",
        }
        if movie["year"]:
            parameters["year"] = movie["year"]

        return "http://www.myapifilms.com/title?" + urlencode(parameters)

    def get_movie_data(self, movie):
        url = self.get_url(movie)
        APP.debug("Fetching url: %s" % url)
        data = self.parse_json(url, path="0")
        if not data:
            return None, {}

        data = self.transform_data(data)
        return data["id"], data

    def get_data_mapping(self):
        return {
            "id": "idIMDB",
            "title": "title",
            "plot": "simplePlot",
            "genre": "genres",
            "director": "directors.0.name",
            "country": "countries",
            "language": "languages",
            "runtime": "runtime",
            "released": "releaseDate",
            "age_rating": "rated",
            "year": "year",
            "metacritic_rating": "metascore",
            "imdb_url": "urlIMDB",
            "imdb_poster": "urlPoster",
            "imdb_rating": "rating",
            "imdb_rating_votes": lambda data: re.sub(r"[^\d]", "", data["rating"]),
        }
