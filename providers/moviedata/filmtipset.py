from providers.moviedata.provider import MoviedataProvider
from application import ACCESS_KEYS, APPLICATION as APP
try:
    from urllib import urlencode  # Python 2.X
except ImportError:
    from urllib.parse import urlencode  # Python 3+

IDENTIFIER = "Filmtipset"

class Provider(MoviedataProvider):
    def get_url(self, movie):
        options = {
            "action": "search",
            "id": movie["name"].encode("utf-8"),
            "returntype": "json",
            "accesskey": ACCESS_KEYS[IDENTIFIER]["ACCESS_KEY"],
            "usernr": ACCESS_KEYS[IDENTIFIER]["USER_KEY"],
        }
        return "http://www.filmtipset.se/api/api.cgi?" + urlencode(options)

    def fetch_movie_data(self, movie):
        url = self.get_url(movie)
        APP.debug("Fetching url: %s" % url)
        data = self.parse_json(url, path="0.data.0.hits")
        data = self.find_movie_matching_year(data, movie["year"])

        if not data:
            return {}

        return self.transform_data(data)

    def find_movie_matching_year(self, data, year):
        if not year:
            return self.traverse_json(data, path="0.movie")

        for i in range(len(data)):
            new_data = self.traverse_json(data, path="%s.movie" % i)
            if new_data.get("year", None) == year:
                return new_data

        return self.traverse_json(data, path="0.movie")

    def get_data_mapping(self):
        return {
            "id": lambda data: "tt" + data["imdb"],
            "title": lambda data: data["orgname"].strip(),
            "title_swe": lambda data: data["name"].strip(),
            "country": "country",
            "director": "director",
            "year": "year",
            "filmtipset_my_grade": "grade.value",
            "filmtipset_my_grade_type": "grade.type",
            "filmtipset_avg_grade": "filmtipsetgrade.value",
            "filmtipset_url": "url",
            "filmtipset_id": "id",
        }
