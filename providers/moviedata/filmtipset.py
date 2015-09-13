from providers.moviedata.provider import MoviedataProvider
from urllib import urlencode
from settings import ACCESS_KEYS
from application import APPLICATION as APP

IDENTIFIER = "Filmtipset"

class Provider(MoviedataProvider):
    def get_movie_data(self, movie):
        options = {
            "action": "search",
            "id": movie["name"],
            "returntype": "json",
            "accesskey": ACCESS_KEYS[IDENTIFIER]["ACCESS_KEY"],
            "usernr": ACCESS_KEYS[IDENTIFIER]["USER_KEY"],
        }
        url = "http://www.filmtipset.se/api/api.cgi?" + urlencode(options)
        APP.debug("Fetching url: %s" % url)
        data = self.parse_json(url, path="0.data.0.hits.0.movie")
        if not data:
            return None, {}

        data = self.transform_data(data)
        return data["id"], data

    def get_data_mapping(self):
        return {
            "id": lambda data: "tt" + data["imdb"],
            "title": "orgname",
            "title_swe": "name",
            "country": "country",
            "director": "director",
            "year": "year",
            "filmtipset_my_grade": "grade.value",
            "filmtipset_my_grade_type": "grade.type",
            "filmtipset_avg_grade": "filmtipsetgrade.value",
            "filmtipset_url": "url",
            "filmtipset_id": "id",
        }
