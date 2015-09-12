import re
from providers.moviedata.provider import MoviedataProvider
from urllib import urlencode

IDENTIFIER = "IMDB"

class Provider(MoviedataProvider):
    def get_movie_data(self, name):
        parameters = {
            "title": name,
            "limit": 1,
            "filter": "M",
            "format": "JSON",
        }
        url = "http://www.myapifilms.com/title?" + urlencode(parameters)
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
