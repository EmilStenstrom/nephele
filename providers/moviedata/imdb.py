from providers.moviedata.provider import MoviedataProvider
from urllib import urlencode

IDENTIFIER = "IMDB"

class Provider(MoviedataProvider):
    def get_movie_data(self, name):
        parameters = {
            "title": name,
            "limit": 1,
            "format": "JSON",
        }
        url = "http://www.myapifilms.com/title?" + urlencode(parameters)
        data = self.parse_json(url)
        return data
