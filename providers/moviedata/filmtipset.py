from providers.moviedata.provider import MoviedataProvider
from urllib import urlencode
from settings import ACCESS_KEYS

IDENTIFIER = "Filmtipset"

class Provider(MoviedataProvider):
    def get_movie_data(self, name):
        options = {
            "action": "search",
            "id": name,
            "returntype": "json",
            "accesskey": ACCESS_KEYS[IDENTIFIER]["ACCESS_KEY"],
            "usernr": ACCESS_KEYS[IDENTIFIER]["USER_KEY"],
        }
        url = "http://www.filmtipset.se/api/api.cgi?" + urlencode(options)
        data = self.parse_json(url, "0.data.0.hits.0.movie")
        return data
