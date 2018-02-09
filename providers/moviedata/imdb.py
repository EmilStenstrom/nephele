import re
from providers.moviedata.provider import MoviedataProvider
from application import ACCESS_KEYS, APPLICATION as APP

IDENTIFIER = "MyAPIfilms"

class Provider(MoviedataProvider):
    def get_url(self, movie):
        parameters = {
            "title": movie["name"].encode("utf-8"),
            "limit": 1,
            "filter": "3",
            "format": "json",
        }
        if "year" in movie and movie["year"]:
            parameters["year"] = movie["year"]
            # Note limits are set before filtering, so with limit 1 we get no hits
            parameters["limit"] = 5

        if IDENTIFIER in ACCESS_KEYS:
            parameters["token"] = ACCESS_KEYS[IDENTIFIER]["TOKEN"]

        return "http://www.myapifilms.com/imdb/title?" + self.urlencode(parameters)

    def fetch_movie_data(self, movie):
        url = self.get_url(movie)
        APP.debug("Fetching url: %s" % url)
        data = self.parse_json(url, path="data.movies")
        for hit in data:
            if hit and "releaseDate" in hit and hit["releaseDate"]:
                return self.transform_data(hit)

        return {}

    def _get_clean_rating(self, data):
        if "rating" not in data:
            return ""

        return re.sub(r"[^\d\.]", "", data["rating"])

    def get_data_mapping(self):
        return {
            "id": "idIMDB",
            "title": lambda data: data["title"].replace(u"\u00a0", ""),
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
            "imdb_rating_votes": self._get_clean_rating,
        }
